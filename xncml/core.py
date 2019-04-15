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
                            print(attr)
                            if attr['@name'] == key:
                                attr = attr.update(item)
                                break
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
