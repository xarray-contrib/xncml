import os
import tempfile
from collections import OrderedDict
from pathlib import Path

import pytest

import xncml

here = os.path.abspath(os.path.dirname(__file__))
input_file = os.path.join(here, 'exercise1.ncml')


def test_ncml_dataset_constructor():
    nc = xncml.Dataset(input_file)
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
        nc = xncml.Dataset('example.ncml')


def test_add_variable_attribute():
    nc = xncml.Dataset(input_file)
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


@pytest.mark.parametrize(
    'variable,key,expected, var_index',
    [
        (
            'T',
            'units',
            OrderedDict(
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
                    ('remove', OrderedDict([('@name', 'units'), ('@type', 'attribute')])),
                ]
            ),
            1,
        ),
        (
            'Tidi',
            'unwantedvaribleAttribute',
            OrderedDict(
                [
                    ('@name', 'Tidi'),
                    (
                        'remove',
                        OrderedDict(
                            [('@name', 'unwantedvaribleAttribute'), ('@type', 'attribute')]
                        ),
                    ),
                ]
            ),
            5,
        ),
    ],
)
def test_remove_variable_attribute(variable, key, expected, var_index):
    nc = xncml.Dataset(input_file)
    nc.remove_variable_attribute(variable=variable, key=key)
    res = nc.ncroot['netcdf']['variable'][var_index]
    assert res == expected


def test_rename_variable():
    nc = xncml.Dataset(input_file)
    nc.rename_variable('lat', 'latitude')
    res = nc.ncroot['netcdf']['variable'][2]
    expected = OrderedDict(
        [
            ('@name', 'latitude'),
            ('@shape', 'lat'),
            ('@type', 'float'),
            (
                'attribute',
                OrderedDict([('@name', 'units'), ('@type', 'String'), ('@value', 'degrees_north')]),
            ),
            ('values', '41.0 40.0 39.0'),
            ('@orgName', 'lat'),
        ]
    )

    assert expected == res

    with pytest.warns(UserWarning):
        nc.rename_variable('Temp', 'Temperature')


def test_add_dataset_attribute():
    nc = xncml.Dataset(input_file)
    nc.add_dataset_attribute(key='editedby', value='foo')
    nc.add_dataset_attribute(key='editedby', value='bar')
    expected = [
        OrderedDict([('@name', 'title'), ('@type', 'String'), ('@value', 'Example Data')]),
        OrderedDict([('@name', 'editedby'), ('@type', 'String'), ('@value', 'bar')]),
    ]
    res = nc.ncroot['netcdf']['attribute']
    assert res == expected


def test_remove_dataset_attribute():
    nc = xncml.Dataset(input_file)
    nc.add_dataset_attribute('bar', 'foo')
    nc.remove_dataset_attribute('title')
    nc.remove_dataset_attribute('bar')
    assert nc.ncroot['netcdf']['attribute'] == OrderedDict()

    nc = xncml.Dataset(input_file)
    nc.remove_dataset_attribute('title')
    assert nc.ncroot['netcdf']['attribute'] == OrderedDict()


def test_remove_dataset_variable():
    nc = xncml.Dataset(input_file)
    nc.remove_dataset_variable('rh')
    expected = set(['T', 'lat', 'lon', 'time'])
    res = set([item['@name'] for item in nc.ncroot['netcdf']['variable']])
    assert expected == res


def test_to_ncml():
    nc = xncml.Dataset(input_file)
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
