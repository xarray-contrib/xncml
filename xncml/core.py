import os
from collections import OrderedDict

import xmltodict


class NcmlReader(object):
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
        variables = self.ncroot['netcdf'].get('variable', None)
        if variables:
            for var in variables:
                if var['@name'] == variable:
                    if isinstance(var['attribute'], list):
                        for attr in var['attribute']:
                            if attr['@name'] == key:
                                attr = attr.update(item)
                            else:
                                var['attribute'].append(item)
                                break
                    else:
                        var['attribute'] = var['attribute'].update(item)

        else:
            var['@name'] = variable
            var['attribute'] = item

    def remove_variable_attribute(self, variable, key):
        """ Remove variable attribute """
        variables = self.ncroot['netcdf'].get('variable', None)
        if variables:
            for var in variables:
                if var['@name'] == variable:
                    if isinstance(var['attribute'], list):
                        for attr in var['attribute']:
                            if attr['@name'] == key:
                                var['attribute'].remove(attr)
                                break

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
        attributes = self.ncroot['netcdf'].get('attribute', None)

        if attributes:
            if isinstance(attributes, OrderedDict):
                if attributes['@name'] == key:
                    attributes.clear()

            else:
                for attrs in attributes:
                    if attrs['@name'] == key:
                        attributes.remove(attrs)
                        break

                if len(attributes) == 0:
                    self.ncroot['netcdf']['attribute'] = OrderedDict()

    def remove_dataset_dimension(self, key):
        """ Remove dataset dimension

        Parameters
        ----------
        key : str
            name of the dimension to remove
        """

        dimensions = self.ncroot['netcdf'].get('dimension', None)
        if dimensions and isinstance(dimensions, list):
            for dim in dimensions:
                if dim['@name'] == key:
                    dimensions.remove(dim)

    def remove_dataset_variable(self, key):
        """ Remove dataset variable

        Parameters
        ----------
        key : str
            name of the variable to remove
        """

        variables = self.ncroot['netcdf'].get('variable', None)
        if variables and isinstance(variables, list):
            for var in variables:
                if var['@name'] == key:
                    variables.remove(var)

    def to_ncml(self, path=None):
        if not path:
            path = f'{self.filepath.strip(".ncml")}_updated.ncml'

        xml_output = xmltodict.unparse(self.ncroot, pretty=True)
        with open(path, 'w') as fd:
            fd.write(xml_output)
        print(f'Persisted new ncml file at: {path}')
