"""
# NcML parser for xarray

The `open_ncml` function parse an XML document compliant with the NcML-2.2 schema and returns an xarray Dataset.

The XML is parsed into a Python objects using `xsdata`. The parser converts XML elements into classes instances
defined in an autogenerated data model (`generated.ncml_2_2`). This datamodel was created using:

  ```bash
  xsdata generate -ds NumPy --compound-fields -mll=119 --postponed-annotations  schemas/ncml-2.2.xsd
  ```

The code below converts the NcML instructions into xarray instructions. Not all NcML instructions are currently
supported.


## TODO

Support for these elements is missing:
- <cacheVariable>
- <logicalReduce>
- <logicalSection>
- <logicalSlice>
- <promoteGlobalAttribute>
- <enumTypedef>
- <scanFmrc>

Support for these attributes is missing:
- dateFormatMark
- olderThan
- tiled aggregations
"""


from __future__ import annotations

import datetime as dt
from functools import partial
from warnings import warn
from pathlib import Path

import numpy as np
import xarray as xr
from xsdata.formats.dataclass.parsers import XmlParser

from .generated import (
    Aggregation,
    AggregationType,
    Attribute,
    DataType,
    Dimension,
    EnumTypedef,
    Group,
    Netcdf,
    ObjectType,
    Remove,
    Values,
    Variable,
)

__author__ = "David Huard"
__date__ = "July 2022"
__contact__ = "huard.david@ouranos.ca"


def parse(path: Path) -> Netcdf:
    """
    Parse NcML file using NetCDF datamodel based on NcML-2.2 Schema.

    Parameters
    ----------
    path : Path
      Path to NcML file.

    Returns
    -------
    Netcdf instance.
      Object description of NcML content.
    """
    parser = XmlParser()
    return parser.from_path(path, Netcdf)


def open_ncml(ncml: str | Path) -> xr.Dataset:
    """
    Convert NcML document to a dataset.

    Parameters
    ----------
    ncml : str | Path
      Path to NcML file.

    Returns
    -------
    xr.Dataset
      Dataset holding variables and attributes defined in NcML document.
    """
    # Parse NcML document
    ncml = Path(ncml)
    obj = parse(ncml)

    return read_netcdf(xr.Dataset(), xr.Dataset(), obj, ncml)


def read_netcdf(
    target: xr.Dataset, ref: xr.Dataset, obj: Netcdf, ncml: Path
) -> xr.Dataset:
    """
    Return content of <netcdf> element.

    Parameters
    ----------
    target : xr.Dataset
      Target dataset to be updated with <netcdf>'s content.
    ref : xr.Dataset
      Reference dataset used to copy content into `target`.
    obj : Netcdf
       <netcdf> object description.
    ncml : Path
      Path to NcML document, sometimes required to follow relative links.

    Returns
    -------
    xr.Dataset
      Dataset holding variables and attributes defined in <netcdf> element.
    """
    # Open location if any
    ref = read_ds(obj, ncml) or ref

    # <explicit/> element means that only content specifically mentioned in NcML document is included in dataset.
    if obj.explicit is not None:
        pass
    else:
        # By default, all metadata from the reference dataset is read: <readMetadata/>
        target = ref

    for item in filter_by_class(obj.choice, Aggregation):
        target = read_aggregation(target, item, ncml)

    # Handle <variable>, <attribute> and <remove> elements
    target = read_group(target, ref, obj)

    return target


def read_aggregation(target: xr.Dataset, obj: Aggregation, ncml: Path) -> xr.Dataset:
    """
    Return merged or concatenated content of <aggregation> element.

    Parameters
    ----------
    target : xr.Dataset
      Target dataset to be updated with <netcdf>'s content.
    obj : Aggregation
       <aggregation> object description.
    ncml : Path
      Path to NcML document, sometimes required to follow relative links.

    Returns
    -------
    xr.Dataset
      Dataset holding variables and attributes defined in <aggregation> element.
    """
    from xarray.coding.times import CFDatetimeCoder

    # Names of variables to be aggregated. All variables if undefined.
    names = [v.name for v in filter_by_class(obj.choice, Aggregation.VariableAgg)]

    for attr in obj.promote_global_attribute:
        raise NotImplementedError

    # Create list of datasets to aggregate.
    datasets = []
    closers = []

    for item in obj.netcdf:
        # Open dataset defined in <netcdf>'s `location` attribute
        tar = read_netcdf(xr.Dataset(), ref=xr.Dataset(), obj=item, ncml=ncml)
        closers.append(getattr(tar, "_close"))

        # Select variables
        if names:
            tar = tar[names]

        # Handle coordinate values
        if item.coord_value is not None:
            dtypes = [
                i[obj.dim_name].dtype.type for i in [tar, target] if obj.dim_name in i
            ]
            coords = read_coord_value(item, obj, dtypes=dtypes)
            tar = tar.assign_coords({obj.dim_name: coords})
        datasets.append(tar)

    # Handle <scan> element
    for item in obj.scan:
        dss = read_scan(item, ncml)
        datasets.extend([ds.chunk() for ds in dss])
        closers.extend([getattr(ds, "_close") for ds in dss])

    # Need to decode time variable
    if obj.time_units_change:
        for i, ds in enumerate(datasets):
            t = xr.as_variable(
                ds[obj.dim_name], obj.dim_name
            )  # Maybe not the same name...
            encoded = CFDatetimeCoder(use_cftime=True).decode(t, name=t.name)
            datasets[i] = ds.assign_coords({obj.dim_name: encoded})

    # Translate different types of aggregation into xarray instructions.
    if obj.type == AggregationType.JOIN_EXISTING:
        agg = xr.concat(datasets, obj.dim_name)
    elif obj.type == AggregationType.JOIN_NEW:
        agg = xr.concat(datasets, obj.dim_name)
    elif obj.type == AggregationType.UNION:
        agg = xr.merge(datasets)
    else:
        raise NotImplementedError

    agg = read_group(agg, None, obj)
    out = target.merge(agg, combine_attrs="no_conflicts")
    out.set_close(partial(_multi_file_closer, closers))
    return out


def read_ds(obj: Netcdf, ncml: Path) -> xr.Dataset:
    """
    Return dataset defined in <netcdf> element.

    Parameters
    ----------
    obj : Netcdf
      <netcdf> object description.
    ncml : Path
      Path to NcML document, sometimes required to follow relative links.

    Returns
    -------
    xr.Dataset
      Dataset defined at <netcdf>' `location` attribute.
    """
    if obj.location:
        try:
            # Python >= 3.9
            location = obj.location.removeprefix("file:")
        except AttributeError:
            location = obj.location.strip("file:")

        if not Path(location).is_absolute():
            location = ncml.parent / location
        return xr.open_dataset(location, decode_times=False)


def read_group(
    target: xr.Dataset, ref: xr.Dataset, obj: Group | Netcdf, dims: dict = None
) -> xr.Dataset:
    """
    Parse <group> items, typically <dimension>, <variable>, <attribute> and <remove> elements.

    Parameters
    ----------
    target : xr.Dataset
      Target dataset to be updated.
    ref : xr.Dataset
      Reference dataset used to copy content into `target`.
    obj : Group | Netcdf
       <netcdf> object description.

    Returns
    -------
    xr.Dataset
      Dataset holding variables and attributes defined in <netcdf> element.
    """
    dims = {} if dims is None else dims
    enums = {}
    for item in obj.choice:
        if isinstance(item, Dimension):
            dims[item.name] = read_dimension(item)
        elif isinstance(item, Variable):
            target = read_variable(target, ref, item, dims, enums)
        elif isinstance(item, Attribute):
            read_attribute(target, item, ref)
        elif isinstance(item, Remove):
            target = read_remove(target, item)
        elif isinstance(item, EnumTypedef):
            enums[item.name] = read_enum(item)
        elif isinstance(item, Group):
            target = read_group(target, ref, item, dims)
        elif isinstance(item, Aggregation):
            pass  # <aggregation> elements are parsed in `read_netcdf`
        else:
            raise AttributeError

    return target


def read_scan(obj: Aggregation.Scan, ncml: Path) -> list[xr.Dataset]:
    """
    Return list of datasets defined in <scan> element.

    Parameters
    ----------
    obj : Aggregation.Scan instance
      <scan> object description.
    ncml : Path
      Path to NcML document, sometimes required to follow relative links.

    Returns
    -------
    list
      List of datasets found by scan.
    """
    import glob
    import re

    if obj.date_format_mark:
        raise NotImplementedError

    path = Path(obj.location)
    if not path.is_absolute():
        path = ncml.parent / path

    files = list(path.rglob("*") if obj.subdirs else path.glob("*"))

    if not files:
        raise ValueError(f"No files found in {path}")

    fns = map(str, files)
    if obj.reg_exp:
        pat = re.compile(obj.reg_exp)
        files = list(filter(pat.match, fns))
    elif obj.suffix:
        pat = "*" + obj.suffix
        files = glob.fnmatch.filter(fns, pat)

    if not files:
        raise ValueError("regular expression or suffix matches no file.")

    files.sort()

    return [xr.open_dataset(f, decode_times=False) for f in files]


def read_coord_value(nc: Netcdf, agg: Aggregation, dtypes: list = ()):
    """
    Read `coordValue` attribute of <netcdf> element.

    Parameters
    ----------
    nc : Netcdf instance
      <netcdf> object description.
    agg : Aggregation instance
      <aggregation> object description
    dtypes : tuple
      List of preferred type for coordinate value.

    Returns
    -------
    str, np.array, scalar
      Coordinate value cast to proper type.

    Notes
    -----
    The casting logic is most likely not up to spec.
    """
    val = nc.coord_value

    # A JOIN_NEW aggregation has exactly one coordinate value
    if agg.type == AggregationType.JOIN_NEW:
        coord = val
    elif agg.type == AggregationType.JOIN_EXISTING:
        coord = val.replace(",", " ").split()
    else:
        raise NotImplementedError

    # Cast to dtype, not clear what the spec is exactly for this.
    if dtypes:
        typ = dtypes[0]
    else:
        try:
            dt.datetime.strptime(coord, "%Y-%m-%d %H:%M:%SZ")
            typ = str
        except ValueError:
            typ = np.float64

    return typ(coord)


def read_enum(obj: EnumTypedef) -> dict[str, list]:
    """
    Parse <enumTypeDef> element.

    Example
    -------
    <enumTypedef name="trilean" type="enum1">
        <enum key="0">false</enum>
        <enum key="1">true</enum>
        <enum key="2">undefined</enum>
    </enumTypedef>

    Parameters
    ----------
    obj: EnumTypeDef
      <enumTypeDef> object.

    Returns
    -------
    dict:
        A dictionary with CF flag_values and flag_meanings that describe the Enum.
    """
    return {
        "flag_values": list(map(lambda e: e.key, obj.content)),
        "flag_meanings": list(map(lambda e: e.content[0], obj.content)),
    }


def read_variable(
    target: xr.Dataset, ref: xr.Dataset, obj: Variable, dimensions: dict, enums: dict
):
    """
    Parse <variable> element.

    Parameters
    ----------
    target : xr.Dataset
      Target dataset to be updated.
    ref : xr.Dataset
      Reference dataset used to copy content into `target`.
    obj : Variable
       <variable> object description.
    dimensions : dict
      Dimension attributes keyed by name.
    enums: dict[str, dict]

    Returns
    -------
    xr.Dataset
      Dataset holding variable defined in <variable> element.
    """
    # Handle logic for variable name change
    if obj.org_name:
        if obj.org_name in target:
            target = target.rename({obj.org_name: obj.name})
            ref_var = None
        elif obj.org_name in ref:
            ref_var = xr.as_variable(ref[obj.org_name])
        else:
            raise ValueError
    else:
        ref_var = None

    # Read existing data or create empty DataArray
    if (obj.name in target) or (obj.name in target.dims):
        out = xr.as_variable(target[obj.name])
        if obj.type:
            out = out.astype(nctype(obj.type))
        ref_var = None
    elif (obj.name in ref) or (obj.name in ref.dims):
        out = xr.as_variable(ref[obj.name])
        if obj.type:
            out = out.astype(nctype(obj.type))
        ref_var = ref[obj.name]
    elif obj.shape:
        dims = obj.shape.split(" ")
        shape = [dimensions[dim].length for dim in dims]
        out = xr.Variable(data=np.empty(shape, dtype=nctype(obj.type)), dims=dims)
    elif obj.shape == "":
        out = build_scalar_variable(
            var_name=obj.name, values_tag=obj.values, var_type=obj.type
        )
    else:
        error_msg = f"Could not build variable `{obj.name}`."
        raise ValueError(error_msg)

    # Set variable attributes
    for item in obj.attribute:
        read_attribute(out, item, ref=ref_var)

    # Remove attributes or dimensions
    for item in obj.remove:
        read_remove(out, item)

    # Read values for arrays (already done for a scalar)
    if obj.values and obj.shape != "":
        data = read_values(obj.name, out.size, obj.values)
        data = out.dtype.type(data)
        out = xr.Variable(
            out.dims,
            data,
            out.attrs,
        )

    if obj.logical_section:
        raise NotImplementedError

    if obj.logical_slice:
        raise NotImplementedError

    if obj.logical_reduce:
        raise NotImplementedError

    if obj.typedef in enums.keys():
        # TODO: Also update encoding when https://github.com/pydata/xarray/pull/8147
        #       is merged in xarray.
        out.attrs["flag_values"] = enums[obj.typedef]["flag_values"]
        out.attrs["flag_meanings"] = enums[obj.typedef]["flag_meanings"]
    elif obj.typedef is not None:
        raise NotImplementedError

    target[obj.name] = out
    return target


def read_values(var_name: str, expected_size: int, values_tag: Values) -> list:
    """Read values for <variable> element.

    Parameters
    ----------
    var_name : str
      The variable name.
    size: int
      The variable expected size.
    values_tag : Values instance
      <values> object description

    Returns
    -------
    list
      A list filled with values from <values> element.
    """
    if values_tag.from_attribute is not None:
        error_msg = (
            "xncml cannot yet fetch values from a global or a "
            f" variable attribute using <from_attribute>, here on variable {var_name}."
        )
        raise NotImplementedError(error_msg)
    if values_tag.start is not None and values_tag.increment is not None:
        number_of_values = int(values_tag.npts or expected_size)
        return values_tag.start + np.arange(number_of_values) * values_tag.increment
    if not isinstance(values_tag.content, list):
        error_msg = f"Unsupported format of the <values> tag from variable {var_name}."
        raise NotImplementedError(error_msg)
    if len(values_tag.content) == 0:
        error_msg = (
            f"No values found for variable {var_name}, but a {expected_size}"
            " values were expected."
        )
        raise ValueError(error_msg)
    if not isinstance(values_tag.content[0], str):
        error_msg = f"Unsupported format of the <values> tag from variable {var_name}."
        raise NotImplementedError(error_msg)
    separator = values_tag.separator or " "
    data = values_tag.content[0].split(separator)
    if len(data) > expected_size:
        error_msg = (
            f"The expected size for variable {var_name} was {expected_size},"
            f" but {len(data)} values were found in its <values> tag."
        )
        raise ValueError(error_msg)
    return data


def build_scalar_variable(
    var_name: str, values_tag: Values, var_type: str
) -> xr.Variable:
    """Read values for <variable> element.

    Parameters
    ----------
    var_name : str
      The variable name.
    values_tag : Values instance
      <values> object description
    var_type: str
      The variable expected type.

    Returns
    -------
    xr.Variable
      A xr.Variable filled with values from <values> element.

    Raises
    ------
    ValueError
      If the <values> tag is not a valid scalar.
    """
    if values_tag is None:
        warn(
            f"Could not set the type for the scalar variable {var_name}, as its"
            " <values> is empty. Provide a single values within <values></values>"
            " to preserve the type."
        )
        return xr.Variable(data=None, dims=())
    values_content = read_values(var_name, expected_size=1, values_tag=values_tag)
    if len(values_content) == 1:
        return xr.Variable(
            data=np.array(values_content[0], dtype=nctype(var_type))[()], dims=()
        )
    if len(values_content) > 1:
        error_msg = (
            f"Multiple values found for variable {var_name} but its"
            ' shape is "" thus a single scalar is expected within its <values> tag.'
        )
    raise ValueError(error_msg)


def read_remove(target: xr.Dataset | xr.Variable, obj: Remove) -> xr.Dataset:
    """Remove item from dataset.

    Parameters
    ----------
    target : xr.Dataset | xr.Variable
      Target dataset or variable to be updated.
    obj : Remove instance
      <remove> object description.

    Returns
    -------
    xr.Dataset or xr.Variable
      Dataset with attribute, variable or dimension removed, or variable with attribute removed.
    """

    if obj.type == ObjectType.ATTRIBUTE:
        target.attrs.pop(obj.name)
    elif obj.type == ObjectType.VARIABLE:
        target = target.drop_vars(obj.name)
    elif obj.type == ObjectType.DIMENSION:
        target = target.drop_dims(obj.name)

    return target


def read_attribute(
    target: xr.Dataset | xr.Variable, obj: Attribute, ref: xr.Dataset = None
):
    """Update target dataset in place with new or modified attribute.

    Parameters
    ----------
    target : xr.Dataset | xr.Variable
      Target dataset to be updated.
    obj : Attribute instance
      <attribute> object description.
    ref : xr.Dataset
      Reference dataset.
    """
    if obj.value is not None:
        target.attrs[obj.name] = cast(obj)
    elif obj.org_name is not None:
        try:
            target.attrs[obj.name] = ref.attrs[obj.org_name]
        except (AttributeError, KeyError):
            target.attrs[obj.name] = target.attrs.get(obj.org_name)
        target.attrs.pop(obj.org_name)
    elif ref is not None:
        target.attrs[obj.name] = ref.attrs.get(obj.name)
    else:
        raise NotImplementedError


def read_dimension(obj: Dimension) -> Dimension:
    """Return dimension object with its length cast to an integer."""
    if obj.length is not None:
        obj.length = int(obj.length)

    return obj


def nctype(typ: DataType) -> type:
    """Return Python type corresponding to the NcML DataType of object."""

    if typ in [DataType.STRING, DataType.STRING_1]:
        return str
    elif typ in [DataType.BYTE, DataType.ENUM1]:
        return np.int8
    elif typ in [DataType.SHORT, DataType.ENUM2]:
        return np.int16
    elif typ in [DataType.INT, DataType.ENUM4]:
        return np.int32
    elif typ == DataType.LONG:
        return int
    elif typ == DataType.FLOAT:
        return np.float32
    elif typ == DataType.DOUBLE:
        return np.float64
    elif typ == DataType.UBYTE:
        return np.ubyte
    elif typ == DataType.USHORT:
        return np.ushort
    elif typ == DataType.UINT:
        return np.uintc
    elif typ == DataType.LONG:
        return np.uint

    raise NotImplementedError


def cast(obj: Attribute) -> tuple | str:
    """Cast attribute value to the appropriate type."""
    value = obj.value or obj.content
    if value:
        if obj.type in [DataType.STRING, DataType.STRING_1]:
            return value

        sep = obj.separator or " "
        values = value.split(sep)
        return tuple(map(nctype(obj.type), values))
    return ""


def filter_by_class(iterable, klass):
    """Return generator filtering on class."""
    for item in iterable:
        if isinstance(item, klass):
            yield item


def _multi_file_closer(closers):
    """Close multiple files."""
    # Note that if a closer is None, it probably means an alteration was made to the original dataset. Make sure
    # that the `_close` attribute is obtained directly from the object returned by `open_dataset`.
    for closer in closers:
        if closer is not None:
            closer()
