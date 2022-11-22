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


__author__ = 'David Huard'
__date__ = 'July 2022'
__contact__ = 'huard.david@ouranos.ca'


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


def read_netcdf(target: xr.Dataset, ref: xr.Dataset, obj: Netcdf, ncml: Path) -> xr.Dataset:
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

    # Create list of items to aggregate.
    items = []
    for item in obj.netcdf:
        # Open dataset defined in <netcdf>'s `location` attribute
        tar = read_netcdf(xr.Dataset(), ref=xr.Dataset(), obj=item, ncml=ncml)

        # Select variables
        if names:
            tar = tar[names]

        # Handle coordinate values
        if item.coord_value is not None:
            dtypes = [i[obj.dim_name].dtype.type for i in [tar, target] if obj.dim_name in i]
            coords = read_coord_value(item, obj, dtypes=dtypes)
            tar = tar.assign_coords({obj.dim_name: coords})
        items.append(tar)

    # Handle <scan> element
    for item in obj.scan:
        items.extend(read_scan(item, ncml))

    # Need to decode time variable
    if obj.time_units_change:
        for i, ds in enumerate(items):
            t = xr.as_variable(ds[obj.dim_name], obj.dim_name)  # Maybe not the same name...
            encoded = CFDatetimeCoder(use_cftime=True).decode(t, name=t.name)
            items[i] = ds.assign_coords({obj.dim_name: encoded})

    # Translate different types of aggregation into xarray instructions.
    if obj.type == AggregationType.JOIN_EXISTING:
        agg = xr.concat(items, obj.dim_name)
    elif obj.type == AggregationType.JOIN_NEW:
        agg = xr.concat(items, obj.dim_name)
    elif obj.type == AggregationType.UNION:
        agg = xr.merge(items)
    else:
        raise NotImplementedError

    agg = read_group(agg, None, obj)
    return target.merge(agg, combine_attrs='no_conflicts')


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
            location = obj.location.removeprefix('file:')
        except AttributeError:
            location = obj.location.strip('file:')

        if not Path(location).is_absolute():
            location = ncml.parent / location
        return xr.open_dataset(location, decode_times=False)


def read_group(target: xr.Dataset, ref: xr.Dataset, obj: Group | Netcdf) -> xr.Dataset:
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
    dims = {}
    for item in obj.choice:
        if isinstance(item, Dimension):
            dims[item.name] = read_dimension(item)
        elif isinstance(item, Variable):
            target = read_variable(target, ref, item, dims)
        elif isinstance(item, Attribute):
            read_attribute(target, item, ref)
        elif isinstance(item, Remove):
            target = read_remove(target, item)
        elif isinstance(item, EnumTypedef):
            raise NotImplementedError
        elif isinstance(item, Group):
            target = read_group(target, ref, item)
        elif isinstance(item, Aggregation):
            pass  # <aggregation> elements are parsed in `read_netcdf`
        else:
            raise AttributeError

    return target


def read_scan(obj: Aggregation.Scan, ncml: Path) -> [xr.Dataset]:
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

    files = list(path.rglob('*') if obj.subdirs else path.glob('*'))

    if not files:
        raise ValueError(f'No files found in {path}')

    fns = map(str, files)
    if obj.reg_exp:
        pat = re.compile(obj.reg_exp)
        files = list(filter(pat.match, fns))
    elif obj.suffix:
        pat = '*' + obj.suffix
        files = glob.fnmatch.filter(fns, pat)

    if not files:
        raise ValueError('regular expression or suffix matches no file.')

    files.sort()

    return [xr.open_dataset(f, decode_times=False).chunk() for f in files]


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
        coord = val.replace(',', ' ').split()
    else:
        raise NotImplementedError

    # Cast to dtype, not clear what the spec is exactly for this.
    if dtypes:
        typ = dtypes[0]
    else:
        try:
            dt.datetime.strptime(coord, '%Y-%m-%d %H:%M:%SZ')
            typ = str
        except ValueError:
            typ = np.float64

    return typ(coord)


def read_variable(target: xr.Dataset, ref: xr.Dataset, obj: Variable, dimensions: dict):
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
            out = out.astype(nctype(obj))
        ref_var = None
    elif (obj.name in ref) or (obj.name in ref.dims):
        out = xr.as_variable(ref[obj.name])
        if obj.type:
            out = out.astype(nctype(obj))
        ref_var = ref[obj.name]
    elif obj.shape:
        dims = obj.shape.split(' ')
        shape = [dimensions[dim].length for dim in dims]
        out = xr.Variable(data=np.empty(shape, dtype=nctype(obj)), dims=dims)
    else:
        raise ValueError

    # Set variable attributes
    for item in obj.attribute:
        read_attribute(out, item, ref=ref_var)

    # Remove attributes or dimensions
    for item in obj.remove:
        read_remove(out, item)

    # Read values
    if obj.values:
        out = read_values(out, obj.values)

    if obj.logical_section:
        raise NotImplementedError

    if obj.logical_slice:
        raise NotImplementedError

    if obj.logical_reduce:
        raise NotImplementedError

    if obj.typedef:
        raise NotImplementedError

    target[obj.name] = out
    return target


def read_values(v: xr.Variable, obj: Values) -> xr.Variable:
    """Read values for <variable> element.

    Parameters
    ----------
    v : xr.DataArray
      Array whose values are to be updated.
    obj : Values instance
      <values> object description

    Returns
    -------
    xr.Variable
      Array filled with values from <values> element.
    """
    if obj.from_attribute is not None:
        raise NotImplementedError

    n = int(obj.npts or v.size)
    if obj.start is not None and obj.increment is not None:
        data = obj.start + np.arange(n) * obj.increment
    else:
        sep = obj.separator or ' '
        if isinstance(obj.content, list) and isinstance(obj.content[0], str):
            data = obj.content[0].split(sep)
        else:
            raise NotImplementedError

    data = v.dtype.type(data)
    return xr.Variable(v.dims, data, v.attrs)


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


def read_attribute(target: xr.Dataset | xr.Variable, obj: Attribute, ref: xr.Dataset = None):
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


def nctype(obj: [Attribute, Variable]) -> type:
    """Return Python type corresponding to the NcML DataType of object."""

    if obj.type in [DataType.STRING, DataType.STRING_1]:
        return str
    elif obj.type == DataType.BYTE:
        return np.int8
    elif obj.type == DataType.SHORT:
        return np.int16
    elif obj.type == DataType.INT:
        return np.int32
    elif obj.type == DataType.LONG:
        return int
    elif obj.type == DataType.FLOAT:
        return np.float32
    elif obj.type == DataType.DOUBLE:
        return np.float64

    raise NotImplementedError


def cast(obj: Attribute):
    """Cast attribute value to the appropriate type."""
    value = obj.value or obj.content
    if value:
        if obj.type in [DataType.STRING, DataType.STRING_1]:
            return value

        sep = obj.separator or ' '
        values = value.split(sep)
        return tuple(map(nctype(obj), values))


def filter_by_class(iterable, klass):
    """Return generator filtering on class."""
    for item in iterable:
        if isinstance(item, klass):
            yield item
