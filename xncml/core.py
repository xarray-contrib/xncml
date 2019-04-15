import os
from collections import OrderedDict
from warnings import warn

import xmltodict


class Dataset(object):
    """ This is a class for reading and manipulating NcML file
    """

    def __init__(self, filepath):
        """

        Parameters
        -----------

        filepath : str
              file path to dataset NcML file

        """

        self.filepath = filepath
        try:
            with open(filepath) as fd:
                self.ncroot = xmltodict.parse(fd.read())

        except Exception as exc:
            raise exc

    def __repr__(self):
        return xmltodict.unparse(self.ncroot, pretty=True)

    # Variable

    def add_variable_attribute(self, variable, key, value, type_='String'):
        """ Add variable attribute

        Parameters
        ----------
        variable : str
              variable name
        key : str
               attribute name
        value : object
              attribute value. Must be a serializable Python Object
        type_ : str, default: 'String'
               string describing attribute type.

        """
        item = OrderedDict({'@name': key, '@type': type_, '@value': value})
        variables = self.ncroot['netcdf'].get('variable', [])

        if isinstance(variables, OrderedDict):
            variables = [variables]

        if variables:
            for var in variables:
                if var['@name'] == variable:
                    var_attributes = var.get('attribute', [])
                    if isinstance(var_attributes, OrderedDict):
                        var_attributes = [var_attributes]
                    for attr in var_attributes:
                        if attr['@name'] == key:
                            attr = attr.update(item)
                            break
                    else:
                        var_attributes.append(item)
                        var['attribute'] = var_attributes
                    break

            else:
                variables.append(OrderedDict({'@name': variable, 'attribute': item}))

    def remove_variable_attribute(self, variable, key):
        """ Remove variable attribute """
        variables = self.ncroot['netcdf'].get('variable', [])
        item = OrderedDict({'@name': key, '@type': 'attribute'})
        if variables:
            for var in variables:
                if var['@name'] == variable:
                    var['remove'] = item
                    break
            else:
                new_var = OrderedDict({'@name': variable, 'remove': item})
                variables.append(new_var)

    def rename_variable(self, variable, new_name):
        """ Rename variable attribute

        Parameters
        ----------
        variable : str
              original variable name
        new_name : str
              New variable name

        """
        variables = self.ncroot['netcdf'].get('variable', [])
        if variables:
            for var in variables:
                if var['@name'] == variable:
                    var['@name'] = new_name
                    var['@orgName'] = variable
                    break
            else:
                warn(f'No {variable} variable found. Skipping')

    def remove_variable(self, variable):
        """ Remove dataset variable

        Parameters
        ----------
        key : str
            name of the variable to remove
        """
        variables = self.ncroot['netcdf'].get('variable', [])
        removes = self.ncroot['netcdf'].get('remove', [])
        item = OrderedDict({'@name': variable, '@type': 'variable'})
        if variables:
            variables_ = [var['@name'] for var in variables]
            if variable in variables_:
                removes.append(item)
                self.ncroot['netcdf']['remove'] = removes
            else:
                warn(f'No {variable} variable found. Skipping')

    def rename_variable_attribute(self, variable, old_name, new_name):
        variables = self.ncroot['netcdf'].get('variable', [])
        if variables:
            for var in variables:
                if var['@name'] == variable:
                    if isinstance(var['attribute'], OrderedDict):
                        var['attribute'] = [var['attribute']]

                    for attr in var['attribute']:
                        if attr['@name'] == old_name:
                            attr['@name'] = new_name
                            attr['@orgName'] = old_name
                            break
                    else:
                        warn(f'No {old_name} attribute found for {variable} variable. Skipping')

    # Dimensions

    def rename_dimension(self, dimension, new_name):
        dimensions = self.ncroot['netcdf'].get('dimension', [])
        if dimensions:
            for dim in dimensions:
                if dim['@name'] == dimension:
                    dim['@name'] = new_name
                    dim['@orgName'] = dimension
                    break
            else:
                warn(f'No {dimension} dimension found. Skipping')

    # Dataset

    def add_dataset_attribute(self, key, value, type_='String'):
        """ Add dataset attribute
         Parameters
        ----------
        key : str
               attribute name
        value : object
              attribute value. Must be a serializable Python Object
        type_ : str, default: 'String'
               string describing attribute type.

        """
        item = OrderedDict({'@name': key, '@type': type_, '@value': value})
        attributes = self.ncroot['netcdf'].get('attribute', None)
        if attributes:
            if isinstance(attributes, OrderedDict):
                if attributes['@name'] == key:
                    attributes = attributes.update(item)

                else:
                    self.ncroot['netcdf']['attribute'] = [attributes, item]

            else:

                for attr in attributes:
                    if attr['@name'] == key:
                        attr = attr.update(item)
                        break

        else:
            self.ncroot['netcdf']['attribute'] = item

    def remove_dataset_attribute(self, key):
        """ Remove dataset attribute

        Parameters
        ----------
        key : str
            Name of the attribute to remove

        """
        removals = self.ncroot['netcdf'].get('remove', [])
        item = OrderedDict({'@name': key, '@type': 'attribute'})
        if isinstance(removals, OrderedDict):
            removals = [removals]

        if removals:
            removals_keys = [
                removal['@name'] for removal in removals if removal['@type'] == 'attribute'
            ]
            if key not in removals_keys:
                removals.append(item)
        else:
            self.ncroot['netcdf']['remove'] = [item]

    def to_ncml(self, path=None):
        if not path:
            path = f'{self.filepath.strip(".ncml")}_modified.ncml'

        xml_output = xmltodict.unparse(self.ncroot, pretty=True)
        with open(path, 'w') as fd:
            fd.write(xml_output)
        print(f'Persisted modified ncml file at: {path}')
