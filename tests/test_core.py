import os
import tempfile
from collections import OrderedDict
from pathlib import Path

import pytest

import xncml


here = os.path.abspath(os.path.dirname(__file__))
input_file = Path(here) / "data" / "exercise1.ncml"


def test_ncml_dataset_constructor():
    # Test with existing NcML
    nc = xncml.Dataset(input_file)
    expected = OrderedDict(
        [
            ("@name", "T"),
            ("@shape", "time lat lon"),
            ("@type", "double"),
            (
                "attribute",
                [
                    OrderedDict(
                        [
                            ("@name", "long_name"),
                            ("@type", "String"),
                            ("@value", "surface temperature"),
                        ]
                    ),
                    OrderedDict([("@name", "units"), ("@type", "String"), ("@value", "C")]),
                ],
            ),
        ]
    )
    res = nc.ncroot["netcdf"]["variable"][1]
    assert res == expected

    # Test with non-existing NcML
    nc = xncml.Dataset("example.ncml")
    assert "@xmlns" in nc.ncroot["netcdf"]

    # Test with non-exising NcML and location
    nc = xncml.Dataset("example.ncml", location=Path(here) / "data" / "nc" / "example1.nc")
    assert "example1.nc" in nc.ncroot["netcdf"]["@location"]

    # Test with namespace
    nc = xncml.Dataset(Path(here) / "data" / "testReadHttps.xml")
    assert nc.ncroot["netcdf"]["attribute"][0]["@value"] == "Example Data"


def test_add_variable_attribute():
    nc = xncml.Dataset(input_file)
    nc.add_variable_attribute(variable="T", key="container", value="ndarray")
    expected = OrderedDict(
        [
            ("@name", "T"),
            ("@shape", "time lat lon"),
            ("@type", "double"),
            (
                "attribute",
                [
                    OrderedDict(
                        [
                            ("@name", "long_name"),
                            ("@type", "String"),
                            ("@value", "surface temperature"),
                        ]
                    ),
                    OrderedDict([("@name", "units"), ("@type", "String"), ("@value", "C")]),
                    OrderedDict([("@name", "container"), ("@type", "String"), ("@value", "ndarray")]),
                ],
            ),
        ]
    )

    res = nc.ncroot["netcdf"]["variable"][1]
    assert res == expected

    nc.add_variable_attribute(variable="Tasmax", key="units", value="kelvin")
    res = nc.ncroot["netcdf"]["variable"][5]
    expected = OrderedDict(
        [
            ("@name", "Tasmax"),
            (
                "attribute",
                OrderedDict([("@name", "units"), ("@type", "String"), ("@value", "kelvin")]),
            ),
        ]
    )
    assert res == expected


@pytest.mark.parametrize(
    "variable,key,expected, var_index",
    [
        (
            "T",
            "units",
            OrderedDict(
                [
                    ("@name", "T"),
                    ("@shape", "time lat lon"),
                    ("@type", "double"),
                    (
                        "attribute",
                        [
                            OrderedDict(
                                [
                                    ("@name", "long_name"),
                                    ("@type", "String"),
                                    ("@value", "surface temperature"),
                                ]
                            ),
                            OrderedDict([("@name", "units"), ("@type", "String"), ("@value", "C")]),
                        ],
                    ),
                    ("remove", OrderedDict([("@name", "units"), ("@type", "attribute")])),
                ]
            ),
            1,
        ),
        (
            "Tidi",
            "unwantedvaribleAttribute",
            OrderedDict(
                [
                    ("@name", "Tidi"),
                    (
                        "remove",
                        OrderedDict([("@name", "unwantedvaribleAttribute"), ("@type", "attribute")]),
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
    res = nc.ncroot["netcdf"]["variable"][var_index]
    assert res == expected


def test_rename_variable():
    # Rename existing variable
    nc = xncml.Dataset(input_file)
    nc.rename_variable("lat", "latitude")
    res = nc.ncroot["netcdf"]["variable"][2]
    expected = OrderedDict(
        [
            ("@name", "latitude"),
            ("@shape", "lat"),
            ("@type", "float"),
            (
                "attribute",
                [
                    OrderedDict([("@name", "units"), ("@type", "String"), ("@value", "degrees_north")]),
                ],
            ),
            ("values", "41.0 40.0 39.0"),
            ("@orgName", "lat"),
        ]
    )

    assert expected == res

    # Rename non-existing variable
    nc.rename_variable("Temp", "Temperature")
    res = nc.ncroot["netcdf"]["variable"][-1]
    assert res == OrderedDict([("@name", "Temperature"), ("@orgName", "Temp")])


def test_rename_variable_attribute():
    # Rename existing attribute
    nc = xncml.Dataset(input_file)
    expected = [
        OrderedDict(
            [
                ("@name", "Units"),
                ("@type", "String"),
                ("@value", "degrees_north"),
                ("@orgName", "units"),
            ]
        )
    ]

    nc.rename_variable_attribute("lat", "units", "Units")
    res = nc.ncroot["netcdf"]["variable"][2]["attribute"]
    assert res == expected

    # Rename non-existing attribute (could be in netCDF file but not in NcML)
    nc.rename_variable_attribute("lat", "foo", "bar")
    res = nc.ncroot["netcdf"]["variable"][2]["attribute"]
    assert {"@name": "bar", "@orgName": "foo"} in res


def test_rename_dimension():
    nc = xncml.Dataset(input_file)
    nc.rename_dimension("time", "Time")
    res = nc.ncroot["netcdf"]["dimension"]
    expected = [
        OrderedDict([("@name", "Time"), ("@length", "2"), ("@isUnlimited", "true"), ("@orgName", "time")]),
        OrderedDict([("@name", "lat"), ("@length", "3")]),
        OrderedDict([("@name", "lon"), ("@length", "4")]),
    ]

    assert res == expected

    # With non-existing dimension
    nc.rename_dimension("time_bound", "time_bounds")
    assert "@orgName" in res[-1]


def test_add_dataset_attribute():
    nc = xncml.Dataset(input_file)
    nc.add_dataset_attribute(key="editedby", value="foo")
    nc.add_dataset_attribute(key="editedby", value="bar")
    expected = [
        OrderedDict([("@name", "title"), ("@type", "String"), ("@value", "Example Data")]),
        OrderedDict([("@name", "editedby"), ("@type", "String"), ("@value", "bar")]),
    ]
    res = nc.ncroot["netcdf"]["attribute"]
    assert res == expected


def test_remove_dataset_attribute():
    nc = xncml.Dataset(input_file)
    nc.add_dataset_attribute("bar", "foo")
    nc.remove_dataset_attribute("title")
    nc.remove_dataset_attribute("title")
    nc.remove_dataset_attribute("bar")
    expected_removals = nc.ncroot["netcdf"]["remove"]
    expected_removals = [removal for removal in expected_removals if removal["@type"] == "attribute"]
    assert len(expected_removals) == 2


def test_rename_dataset_attribute():
    nc = xncml.Dataset(input_file)
    # Rename existing attribute
    nc.rename_dataset_attribute(old_name="title", new_name="Title")
    assert nc.ncroot["netcdf"]["attribute"][0]["@name"] == "Title"

    # Rename attribute not in the NcML (but possibly in the netcdf `location`)
    nc.rename_dataset_attribute(old_name="foo", new_name="bar")
    assert nc.ncroot["netcdf"]["attribute"][1]["@name"] == "bar"


def test_remove_variable():
    nc = xncml.Dataset(input_file)
    nc.remove_variable("lon")
    expected = [OrderedDict([("@name", "lon"), ("@type", "variable")])]
    res = nc.ncroot["netcdf"]["remove"]
    assert expected == res


def test_add_aggregation():
    nc = xncml.Dataset(input_file)
    nc.add_aggregation("new_dim", "joinNew")
    nc.add_variable_agg("new_dim", "newVar")

    expected = [
        OrderedDict(
            [
                ("@dimName", "new_dim"),
                ("@type", "joinNew"),
                ("variableAgg", [OrderedDict([("@name", "newVar")])]),
            ]
        )
    ]
    res = nc.ncroot["netcdf"]["aggregation"]

    assert expected == res


def test_add_scan():
    nc = xncml.Dataset(input_file)
    nc.add_aggregation("new_dim", "joinExisting")
    nc.add_scan("new_dim", location="foo", suffix=".nc")

    expected = [
        OrderedDict(
            [
                ("@dimName", "new_dim"),
                ("@type", "joinExisting"),
                (
                    "scan",
                    [OrderedDict([("@location", "foo"), ("@subdirs", "true"), ("@suffix", ".nc")])],
                ),
            ]
        )
    ]

    res = nc.ncroot["netcdf"]["aggregation"]
    assert expected == res


def test_to_ncml():
    nc = xncml.Dataset(input_file)
    with tempfile.NamedTemporaryFile(suffix=".ncml") as t:
        nc.to_ncml(path=t.name)
        assert os.path.exists(t.name)

    nc.to_ncml()
    default = f"{str(input_file).strip('.ncml')}_modified.ncml"
    assert os.path.exists(default)
    try:
        os.remove(default)
    except Exception:
        pass


def test_to_dict():
    nc = xncml.Dataset(input_file)
    out = nc.to_cf_dict()
    assert out["attributes"]["title"] == "Example Data"
    assert out["variables"]["rh"]["attributes"]["long_name"] == "relative humidity"
    assert out["variables"]["rh"]["type"] == "int"
    assert out["variables"]["rh"]["shape"] == ["time", "lat", "lon"]
    assert out["dimensions"]["time"] == 2
    assert "groups" not in out

    # Check coordinates are first
    assert list(out["variables"].keys())[:3] == ["lat", "lon", "time"]

    nc = xncml.Dataset(Path(here) / "data" / "aggNewCoord.ncml")
    out = nc.to_cf_dict()
    assert out["variables"]["time"]["data"] == [0, 1, 2]

    nc = xncml.Dataset(Path(here) / "data" / "subsetCoordEdges.ncml")
    with pytest.raises(NotImplementedError):
        nc.to_cf_dict()


def test_from_xml():
    nc1 = xncml.Dataset(input_file)

    xml = input_file.read_text()
    nc2 = xncml.Dataset.from_text(xml)

    assert str(nc2) == str(nc1)
