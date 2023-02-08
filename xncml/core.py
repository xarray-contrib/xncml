from collections import OrderedDict
from pathlib import Path
from typing import Any
from warnings import warn

import xmltodict


class Dataset(object):
    """This is a class for reading and manipulating NcML file.

    Note that NcML documents are used for two distinct purposes:
      - an XML description of NetCDF structure and metadata;
      - create virtual NetCDF datasets, e.g. an aggregation of multiple files.

    This class supports both types of uses.
    """

    def __init__(self, filepath: str = None, location: str = None):
        """

        Parameters
        -----------
        filepath : str
            File path to dataset NcML file. If it does not exist, an empty NcML document will be created and this will
            be the default filename when writing to disk with `to_ncml`.
        location : Str
            NetCDF file location. Set this to create a NcML file modifying an existing NetCDF document.
        """
        self.filepath = Path(filepath) if filepath is not None else None

        if self.filepath and self.filepath.exists():
            # Convert all dictionaries to lists of dicts to simplify the internal logic.
            self.ncroot = xmltodict.parse(
                self.filepath.read_text(),
                force_list=['variable', 'attribute', 'group', 'dimension'],
                process_namespaces=True,
                namespaces={
                    'http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2': None,
                    'https://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2': None,
                },
            )

        else:
            self.ncroot = OrderedDict()
            self.ncroot['netcdf'] = OrderedDict(
                {'@xmlns': 'http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2'}
            )
            if location is not None:
                self.ncroot['netcdf']['@location'] = str(location)

    def __repr__(self):
        return xmltodict.unparse(self.ncroot, pretty=True)

    # Variable

    def add_variable_attribute(self, variable, key, value, type_='String'):
        """Add variable attribute.

        Parameters
        ----------
        variable : str
            Variable name
        key : str
            Attribute name
        value : object
            Attribute value. Must be a serializable Python Object
        type_ : str, default: 'String'
             String describing attribute type.

        """
        item = OrderedDict({'@name': key, '@type': type_, '@value': value})
        variables = self.ncroot['netcdf'].get('variable', [])

        for var in variables:
            if var['@name'] == variable:
                var_attributes = var.get('attribute', [])
                for attr in var_attributes:
                    if attr['@name'] == key:
                        attr.update(item)
                        break
                else:
                    var_attributes.append(item)
                    var['attribute'] = var_attributes
                break
        else:
            variables.append(OrderedDict({'@name': variable, 'attribute': item}))
            self.ncroot['netcdf']['variable'] = variables

    def remove_variable_attribute(self, variable, key):
        """Remove variable attribute"""
        item = OrderedDict({'@name': key, '@type': 'attribute'})
        variables = self.ncroot['netcdf'].get('variable', [])

        for var in variables:
            if var['@name'] == variable:
                var['remove'] = item
                break
        else:
            new_var = OrderedDict({'@name': variable, 'remove': item})
            variables.append(new_var)
            self.ncroot['netcdf']['variable'] = variables

    def rename_variable(self, variable, new_name):
        """Rename variable attribute

        Parameters
        ----------
        variable : str
            Original variable name.
        new_name : str
            New variable name.

        """
        item = OrderedDict({'@name': new_name, '@orgName': variable})
        variables = self.ncroot['netcdf'].get('variable', [])

        for var in variables:
            if var['@name'] == variable:
                var['@name'] = new_name
                var['@orgName'] = variable
                break
        else:
            variables.append(item)
            self.ncroot['netcdf']['variable'] = variables

    def remove_variable(self, variable):
        """Remove dataset variable.

        Parameters
        ----------
        key : str
            Name of the variable to remove.
        """
        item = OrderedDict({'@name': variable, '@type': 'variable'})
        removes = self.ncroot['netcdf'].get('remove', [])

        if item not in removes:
            removes.append(item)
            self.ncroot['netcdf']['remove'] = removes

    def rename_variable_attribute(self, variable, old_name, new_name):
        """Rename variable attribute.

        Parameters
        ----------
        variable : str
          Variable name.
        old_name : str
          Original attribute name.
        new_name : str
          New attribute name.
        """
        item = OrderedDict({'@name': new_name, '@orgName': old_name})
        variables = self.ncroot['netcdf'].get('variable', [])

        for var in variables:
            if var['@name'] == variable:
                attrs = var.get('attribute', [])
                for attr in attrs:
                    if attr['@name'] == old_name:
                        attr['@name'] = new_name
                        attr['@orgName'] = old_name
                        break
                else:
                    attrs.append(item)
                    break
        else:
            new_var = OrderedDict({'@name': 'variable', 'attribute': item})
            variables.append(new_var)
            self.ncroot['netcdf']['variable'] = variables

    # Dimensions

    def rename_dimension(self, dimension, new_name):
        """Rename dimension.

        Parameters
        ----------
        dimension: str
          Original dimension name.
        new_name: str
          New dimension name.
        """
        item = OrderedDict({'@name': new_name, '@orgName': dimension})
        dimensions = self.ncroot['netcdf'].get('dimension', [])

        for dim in dimensions:
            if dim['@name'] == dimension:
                dim['@name'] = new_name
                dim['@orgName'] = dimension
                break
        else:
            dimensions.append(item)
            self.ncroot['netcdf']['dimensions'] = dimensions

    # Dataset

    def add_dataset_attribute(self, key, value, type_='String'):
        """Add dataset attribute
         Parameters
        ----------
        key : str
            Attribute name.
        value : object
            Attribute value. Must be a serializable Python Object.
        type_ : str, default: 'String'
            String describing attribute type.

        """
        item = OrderedDict({'@name': key, '@type': type_, '@value': value})
        attributes = self.ncroot['netcdf'].get('attribute', [])

        for attr in attributes:
            if attr['@name'] == key:
                attr.update(item)
                break
        else:
            attributes.append(item)
            self.ncroot['netcdf']['attribute'] = attributes

    def remove_dataset_attribute(self, key):
        """Remove dataset attribute.

        Parameters
        ----------
        key : str
            Name of the attribute to remove.

        """
        removals = self.ncroot['netcdf'].get('remove', [])
        item = OrderedDict({'@name': key, '@type': 'attribute'})

        if removals:
            removals_keys = [
                removal['@name'] for removal in removals if removal['@type'] == 'attribute'
            ]
            if key not in removals_keys:
                removals.append(item)
        else:
            self.ncroot['netcdf']['remove'] = [item]

    def rename_dataset_attribute(self, old_name, new_name):
        """Rename dataset attribute.

        Parameters
        ----------
        old_name: str
          Original attribute name.
        new_name: str
          New attribute name.
        """

        attributes = self.ncroot['netcdf'].get('attribute', None)
        item = OrderedDict({'@name': new_name, 'orgName': old_name})

        if attributes:
            if isinstance(attributes, (dict, OrderedDict)):
                attributes = [attributes]

            for attr in attributes:
                if attr['@name'] == old_name:
                    attr['@name'] = new_name
                    attr['@orgName'] = old_name
                    break
            else:
                self.ncroot['netcdf']['attribute'] = [*attributes, item]

        else:
            self.ncroot['netcdf']['attribute'] = item

    def to_ncml(self, path=None):
        """Write NcML file to disk.

        Parameters
        ----------
        path: str
          Path to write NcML document.
        """
        if not path:
            if self.filepath.exists():
                path = f'{str(self.filepath).strip(".ncml")}_modified.ncml'
            else:
                path = str(self.filepath)

        xml_output = xmltodict.unparse(self.ncroot, pretty=True)
        with open(path, 'w') as fd:
            fd.write(xml_output)

    def to_cf_dict(self):
        """Convert internal representation to a CF-JSON dictionary.

        The CF-JSON specification includes `data` for variables, but this is not included here.

        Returns
        -------
        Dictionary with `dimensions` and `variables` keys. May also optionally include an `attributes` key and a
        `groups` key. Additional keys prefixed with `@` may be included for <netcdf> tag attributes,
        for example `@location`.

        References
        ----------
        http://cf-json.org/specification
        """
        res = OrderedDict()
        nc = self.ncroot['netcdf']

        for key, val in nc.items():
            if key[0] == '@':
                res[key] = val
            if key == 'dimension':
                res.update(_dims_to_json(val))
            if key == 'group':
                res.update(_groups_to_json(val))
            if key == 'attribute':
                res.update(_attributes_to_json(val))
            if key == 'variable':
                res.update(_variables_to_json(val))

        return res


def _dims_to_json(dims: list) -> dict:
    """The dimensions object has dimension id:size as its key:value members."""
    out = OrderedDict()
    for dim in dims:
        if int(dim['@length']) > 1:
            out[dim['@name']] = int(dim['@length'])

    return {'dimensions': out}


def _groups_to_json(groups: list) -> dict:
    out = OrderedDict()
    for group in groups:
        name = group['@name']
        out[name] = OrderedDict()
        if 'attribute' in group:
            out[name].update(_attributes_to_json(group['attribute']))
        if 'group' in group:
            out[name].update(_groups_to_json(group['group']))

    return {'groups': out}


def _attributes_to_json(attrs: list) -> dict:
    """The attributes object contains arbitrary attributes as its key:value members."""
    SPECIAL_ATTRS = ['missing_value', 'cell_methods']

    out = OrderedDict()
    for attr in attrs:
        if attr['@name'] not in SPECIAL_ATTRS:
            try:
                out[attr['@name']] = _cast(attr)
            except ValueError as exc:
                warn(f"Could not cast {attr['@name']}:\n{exc}")

    return {'attributes': out}


def _variables_to_json(variables: list) -> dict:
    """The variables definition object has variable id:object as its key:value members.

    Each variable object MUST include shape, attributes and data objects.
    The shape field is an array of dimension IDs which correspond to the array ordering of the variable data.
    """
    AXIS_VAR = ['time', 'lat', 'latitude', 'lon', 'longitude', 'site']

    out = OrderedDict()

    # Put axis variables first
    for special_var in AXIS_VAR:
        if special_var in [v['@name'] for v in variables]:
            out[special_var] = None

    for var in variables:
        name = var['@name']
        out[name] = OrderedDict()

        if '@shape' in var:
            out[name]['shape'] = var['@shape'].split(' ')

        if '@type' in var:
            out[name]['type'] = var['@type']

        if 'attribute' in var:
            out[name].update(_attributes_to_json(var['attribute']))

        if 'values' in var:
            out[name]['data'] = _cast(var)

    return {'variables': out}


def _cast(obj: dict) -> Any:
    """Cast attribute value to the appropriate type."""
    from xncml.parser import DataType, nctype

    value = obj.get('@value') or obj.get('values')
    typ = DataType(obj.get('@type', 'String'))
    if value is not None:
        if isinstance(value, str):
            if typ in [DataType.STRING, DataType.STRING_1]:
                return value

            sep = ' '
            values = value.split(sep)
            return list(map(nctype(typ), values))
        elif isinstance(value, dict):
            raise NotImplementedError(obj)
        else:
            return value
