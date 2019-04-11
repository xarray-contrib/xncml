import os
import tempfile
from collections import OrderedDict

import pytest

import xncml

here = os.path.abspath(os.path.dirname(__file__))
input_file = os.path.join(here, 'exercise1.ncml')


def test_ncml_reader_constructor():
    nc = xncml.NcmlReader(input_file)
    expected = OrderedDict(
        [
            ('@name', 'T'),
            ('@shape', 'time lat lon'),
            ('@type', 'double'),
            (
                'attribute',
                [
                    OrderedDict(
                        [
                            ('@name', 'long_name'),
                            ('@type', 'String'),
                            ('@value', 'surface temperature'),
                        ]
                    ),
                    OrderedDict([('@name', 'units'), ('@type', 'String'), ('@value', 'C')]),
                ],
            ),
        ]
    )
    res = nc.ncroot['netcdf']['variable'][1]
    assert res == expected

    with pytest.raises(Exception):
        nc = xncml.NcmlReader('example.ncml')


def test_add_variable_attribute():
    nc = xncml.NcmlReader(input_file)
    nc.add_variable_attribute(variable='T', key='container', value='ndarray')
    expected = OrderedDict(
        [
            ('@name', 'T'),
            ('@shape', 'time lat lon'),
            ('@type', 'double'),
            (
                'attribute',
                [
                    OrderedDict(
                        [
                            ('@name', 'long_name'),
                            ('@type', 'String'),
                            ('@value', 'surface temperature'),
                        ]
                    ),
                    OrderedDict([('@name', 'units'), ('@type', 'String'), ('@value', 'C')]),
                    OrderedDict(
                        [('@name', 'container'), ('@type', 'String'), ('@value', 'ndarray')]
                    ),
                ],
            ),
        ]
    )

    res = nc.ncroot['netcdf']['variable'][1]
    assert res == expected


def test_remove_variable_attribute():
    nc = xncml.NcmlReader(input_file)
    nc.remove_variable_attribute(variable='T', key='units')
    expected = OrderedDict(
        [
            ('@name', 'T'),
            ('@shape', 'time lat lon'),
            ('@type', 'double'),
            (
                'attribute',
                [
                    OrderedDict(
                        [
                            ('@name', 'long_name'),
                            ('@type', 'String'),
                            ('@value', 'surface temperature'),
                        ]
                    )
                ],
            ),
        ]
    )
    res = nc.ncroot['netcdf']['variable'][1]
    assert res == expected


def test_add_dataset_attribute():
    nc = xncml.NcmlReader(input_file)
    nc.add_dataset_attribute(key='editedby', value='foo')
    nc.add_dataset_attribute(key='editedby', value='bar')
    expected = [
        OrderedDict([('@name', 'title'), ('@type', 'String'), ('@value', 'Example Data')]),
        OrderedDict([('@name', 'editedby'), ('@type', 'String'), ('@value', 'bar')]),
    ]
    res = nc.ncroot['netcdf']['attribute']
    assert res == expected


def test_remove_dataset_attribute():
    nc = xncml.NcmlReader(input_file)
    nc.add_dataset_attribute('bar', 'foo')
    nc.remove_dataset_attribute('title')
    nc.remove_dataset_attribute('bar')
    assert nc.ncroot['netcdf']['attribute'] == OrderedDict()

    nc = xncml.NcmlReader(input_file)
    nc.remove_dataset_attribute('title')
    assert nc.ncroot['netcdf']['attribute'] == OrderedDict()


def test_remove_dataset_dimension():
    nc = xncml.NcmlReader(input_file)
    nc.remove_dataset_dimension('time')
    expected = [
        OrderedDict([('@name', 'lat'), ('@length', '3')]),
        OrderedDict([('@name', 'lon'), ('@length', '4')]),
    ]
    res = nc.ncroot['netcdf']['dimension']
    assert expected == res


def test_remove_dataset_variable():
    nc = xncml.NcmlReader(input_file)
    nc.remove_dataset_variable('rh')
    expected = set(['T', 'lat', 'lon', 'time'])
    res = set([item['@name'] for item in nc.ncroot['netcdf']['variable']])
    assert expected == res


def test_to_ncml():
    nc = xncml.NcmlReader(input_file)
    with tempfile.NamedTemporaryFile(suffix='.ncml') as t:
        nc.to_ncml(path=t.name)
        assert os.path.exists(t.name)

    nc.to_ncml()
    default = f'{input_file.strip(".ncml")}_updated.ncml'
    assert os.path.exists(default)
    try:
        os.remove(default)
    except Exception:
        pass
