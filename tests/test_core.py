import os
import tempfile
from collections import OrderedDict
from pathlib import Path

import pytest

import xncml

here = os.path.abspath(os.path.dirname(__file__))
input_file = Path(here) / 'data' / 'exercise1.ncml'


def test_ncml_dataset_constructor():

    # Test with existing NcML
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

    # Test with non-existing NcML
    nc = xncml.Dataset('example.ncml')
    assert '@xmlns' in nc.ncroot['netcdf']

    # Test with non-exising NcML and location
    nc = xncml.Dataset('example.ncml', location=Path(here) / 'data' / 'nc' / 'example1.nc')
    assert 'example1.nc' in nc.ncroot['netcdf']['@location']


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

    nc.add_variable_attribute(variable='Tasmax', key='units', value='kelvin')
    res = nc.ncroot['netcdf']['variable'][5]
    expected = OrderedDict(
        [
            ('@name', 'Tasmax'),
            (
                'attribute',
                OrderedDict([('@name', 'units'), ('@type', 'String'), ('@value', 'kelvin')]),
            ),
        ]
    )
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
    # Rename existing variable
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
                [OrderedDict([('@name', 'units'), ('@type', 'String'), ('@value', 'degrees_north')]),],
            ),
            ('values', '41.0 40.0 39.0'),
            ('@orgName', 'lat'),
        ]
    )

    assert expected == res

    # Rename non-existing variable
    nc.rename_variable('Temp', 'Temperature')
    res = nc.ncroot['netcdf']['variable'][-1]
    assert res == OrderedDict([('@name', 'Temperature'), ('@orgName', 'Temp')])


def test_rename_variable_attribute():
    # Rename existing attribute
    nc = xncml.Dataset(input_file)
    expected = [
        OrderedDict(
            [
                ('@name', 'Units'),
                ('@type', 'String'),
                ('@value', 'degrees_north'),
                ('@orgName', 'units'),
            ]
        )
    ]

    nc.rename_variable_attribute('lat', 'units', 'Units')
    res = nc.ncroot['netcdf']['variable'][2]['attribute']
    assert res == expected

    # Rename non-existing attribute (could be in netCDF file but not in NcML)
    nc.rename_variable_attribute('lat', 'foo', 'bar')
    res = nc.ncroot['netcdf']['variable'][2]['attribute']
    assert {'@name': 'bar', '@orgName': 'foo'} in res


def test_rename_dimension():
    nc = xncml.Dataset(input_file)
    nc.rename_dimension('time', 'Time')
    res = nc.ncroot['netcdf']['dimension']
    expected = [
        OrderedDict(
            [('@name', 'Time'), ('@length', '2'), ('@isUnlimited', 'true'), ('@orgName', 'time')]
        ),
        OrderedDict([('@name', 'lat'), ('@length', '3')]),
        OrderedDict([('@name', 'lon'), ('@length', '4')]),
    ]

    assert res == expected

    # With non-existing dimension
    nc.rename_dimension('time_bound', 'time_bounds')
    assert "@orgName" in res[-1]


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
    nc.remove_dataset_attribute('title')
    nc.remove_dataset_attribute('bar')
    expected_removals = nc.ncroot['netcdf']['remove']
    expected_removals = [
        removal for removal in expected_removals if removal['@type'] == 'attribute'
    ]
    assert len(expected_removals) == 2


def test_remove_variable():
    nc = xncml.Dataset(input_file)
    nc.remove_variable('lon')
    expected = [OrderedDict([('@name', 'lon'), ('@type', 'variable')])]
    res = nc.ncroot['netcdf']['remove']
    assert expected == res


def test_to_ncml():
    nc = xncml.Dataset(input_file)
    with tempfile.NamedTemporaryFile(suffix='.ncml') as t:
        nc.to_ncml(path=t.name)
        assert os.path.exists(t.name)

    nc.to_ncml()
    default = f'{str(input_file).strip(".ncml")}_modified.ncml'
    assert os.path.exists(default)
    try:
        os.remove(default)
    except Exception:
        pass
