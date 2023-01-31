from collections import OrderedDict
from pathlib import Path
from warnings import warn

import xmltodict


class Dataset(object):
    """This is a class for reading and manipulating NcML file"""

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
                process_namespaces=True,
                namespaces={
                    'http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2': None,
                    'https://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2': None,
                },
            )
            for key, item in self.ncroot['netcdf'].items():
                if isinstance(item, (dict, OrderedDict)):
                    self.ncroot['netcdf'][key] = [item]

            if 'variable' in self.ncroot['netcdf']:
                for var in self.ncroot['netcdf']['variable']:
                    for key, item in var.items():
                        if isinstance(item, (dict, OrderedDict)):
                            var[key] = [item]

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

    def to_cf_dict(self, mapping={}):
        """Convert internal representation to a CF-JSON dictionary.

        The CF-JSON specification includes `data` for variables, but this is not included here.

        Parameters
        ----------
        mapping : dict
          Map original variable names to new names.

        Returns
        -------
        Dictionary with `dimensions`, `variables` and `attributes` keys.

        References
        ----------
        http://cf-json.org/specification
        """
        res = OrderedDict()
        nc = self.ncroot["netcdf"]
        AXIS_VAR = ['time', 'lat', 'latitude', 'lon', 'longitude', 'site']
        SPECIAL_ATTRS = ['missing_value', 'cell_methods']

        # Dimensions
        res["dimensions"] = OrderedDict()
        try:
            dims = nc["dimension"]
            for dim in dims:
                if int(dim["@length"]) > 1:
                    res["dimensions"][dim["@name"]] = int(dim["@length"])
        except Exception as exc:
            raise ValueError("Failed to export dimensions.", exc)

        # Attributes
        res['attributes'] = OrderedDict()
        try:
            for att in nc["attribute"]:
                res['attributes'][att["@name"]] = cast(att)

        except Exception as exc:
            raise ValueError(f"Failed to export global attribute {att}", exc)

        # Variables
        res["variables"] = OrderedDict()
        # Put axis variables first
        for special_var in AXIS_VAR:
            if special_var in [v["@name"] for v in nc["variable"]]:
                res['variables'][special_var] = None

        for var in nc["variable"]:
            varout = mapping.get(var["@name"], var["@name"])

            if var["@name"] == "dum1":
                continue
            if var == "time":
                res['variables']['time'] = {
                    'shape': ['time'],
                    'type': 'string',
                    'attributes': {'units': 'ISO8601 datetimes'}
                }
                continue
            try:
                res['variables'][varout] = {'attributes': OrderedDict()}
                res['variables'][varout]['shape'] = var["@shape"]

                for att in var["attribute"]:
                    if att not in SPECIAL_ATTRS:
                        res['variables'][varout]['attributes'][att["@name"]] = cast(att)

            except Exception as exc:
                raise ValueError(f'Failed to export variable {var["@name"]} description or attributes', exc)

        return res

    def to_json(self):
        """Serialize dictionary to JSON."""
        import json
        return json.dump(self.to_cf_dict())


def cast(obj: dict):
    """Cast attribute value to the appropriate type."""
    from xncml.parser import DataType, nctype

    value = obj["@value"]
    typ = DataType(obj["@type"])
    if value:
        if typ in [DataType.STRING, DataType.STRING_1]:
            return value

        sep = ' '
        values = value.split(sep)
        return tuple(map(nctype(obj), values))




