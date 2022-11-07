import pytest
import numpy as np
import datetime as dt
import xncml
from pathlib import Path

"""
# Notes

This is not testing absolute paths. Would need to modify the XML files _live_ to reflect the actual path. 
"""

data = Path(__file__).parent / "data"


def test_aggexisting():
    ds = xncml.open_ncml(data / "aggExisting.xml")
    check_dimension(ds)
    check_coord_var(ds)
    check_agg_coord_var(ds)
    check_read_data(ds)
    assert ds["time"].attrs["ncmlAdded"] == "timeAtt"


def test_aggexisting_w_coords():
    ds = xncml.open_ncml(data / "aggExistingWcoords.xml")
    check_dimension(ds)
    check_coord_var(ds)
    check_agg_coord_var(ds)
    check_read_data(ds)
    assert ds["time"].attrs["ncmlAdded"] == "timeAtt"


def test_aggexisting_coords_var():
    ds = xncml.open_ncml(data / "aggExisting1.xml")
    check_dimension(ds)
    check_coord_var(ds)
    check_agg_coord_var(ds)
    check_read_data(ds)
    assert all(ds["time"].data == list(range(7, 125, 2)))


def test_agg_new():
    ds = xncml.open_ncml(data / "aggNew.ncml")
    assert len(ds.time) == 3
    assert all(ds.time.data == [0, 10, 99])
    assert "T" in ds.data_vars
    assert len(ds.lat) == 3


def test_agg_new_coord():
    ds = xncml.open_ncml(data / "aggNewCoord.ncml")
    assert ds.time.dtype == np.int32
    assert len(ds.time) == 3
    assert all(ds.time.data == [0, 1, 2])
    assert ds.time.attrs["units"] == "months since 2000-6-16 6:00"
    assert "T" in ds.data_vars
    assert len(ds.lat) == 3


def test_agg_existing2():
    ds = xncml.open_ncml(data / "aggExisting2.xml")
    assert ds["time"].attrs["units"] == "hours since 2006-06-16 00:00"
    assert ds["time"].dtype == float
    assert all(ds["time"].data == [12.0, 13.0, 14.0])


def test_agg_existing4():
    ds = xncml.open_ncml(data / "aggExisting4.ncml")
    assert all(ds["time"].data == [1.1496816e9, 1.1496852e9, 1.1496888e9])


def test_agg_existing5():
    ds = xncml.open_ncml(data / "aggExisting5.ncml")
    assert ds["time"].dtype == np.int32
    assert all(ds["time"].data == list(range(59)))


def test_agg_existing_add_coords():
    # TODO: Complete test
    ds = xncml.open_ncml(data / "aggExistingAddCoord.ncml")
    assert "time" in ds.variables


def test_modify_atts():
    ds = xncml.open_ncml(data / "modifyAtts.xml")
    assert ds.attrs["Conventions"] == "Metapps"
    assert "title" not in ds.attrs
    assert "UNITS" in ds["rh"].attrs
    assert "units" not in ds["rh"].attrs
    assert ds["rh"].attrs["longer_name"] == "Abe said what?"
    assert "long_name" not in ds["rh"].attrs


def test_modify_vars():
    ds = xncml.open_ncml(data / "modifyVars.xml")
    assert ds.attrs["Conventions"] == "added"
    assert ds.attrs["title"] == "replaced"

    assert "deltaLat" in ds.data_vars
    assert all(ds["deltaLat"].data == [0.1, 0.1, 0.01])
    assert ds["deltaLat"].dtype == float

    assert "Temperature" in ds.data_vars
    assert "T" not in ds.data_vars

    assert "ReletiveHumidity" in ds.data_vars
    assert "rh" not in ds.data_vars
    rh = ds["ReletiveHumidity"]
    assert rh.attrs["long_name2"] == "relatively humid"
    assert rh.attrs["units"] == "percent (%)"
    assert "long_name" not in rh.attrs


def test_agg_syn_grid():
    ds = xncml.open_ncml(data / "aggSynGrid.xml")
    assert len(ds.lat) == 3
    assert len(ds.lon) == 4
    assert len(ds.time) == 3
    assert all(
        ds.time
        == ["2005-11-22 22:19:53Z", "2005-11-22 23:19:53Z", "2005-11-23 00:19:59Z"]
    )


def test_agg_syn_no_coord():
    ds = xncml.open_ncml(data / "aggSynNoCoord.xml")
    assert len(ds.lat) == 3
    assert len(ds.lon) == 4
    assert len(ds.time) == 3


def test_agg_syn_no_coords_dir():
    ds = xncml.open_ncml(data / "aggSynNoCoordsDir.xml")
    assert len(ds.lat) == 3
    assert len(ds.lon) == 4
    assert len(ds.time) == 3


def test_agg_synthetic():
    ds = xncml.open_ncml(data / "aggSynthetic.xml")
    assert len(ds.time) == 3
    assert all(ds.time == [0, 10, 99])


def test_agg_synthetic_2():
    ds = xncml.open_ncml(data / "aggSynthetic2.xml")
    assert len(ds.time) == 3
    assert all(ds.time == [0, 1, 2])


def test_agg_synthetic_3():
    ds = xncml.open_ncml(data / "aggSynthetic3.xml")
    assert len(ds.time) == 3
    assert all(ds.time == [0, 10, 99])


def test_agg_syn_scan():
    ds = xncml.open_ncml(data / "aggSynScan.xml")
    assert len(ds.time) == 3
    assert all(ds.time == [0, 10, 20])


def test_agg_syn_rename():
    ds = xncml.open_ncml(data / "aggSynRename.xml")
    assert len(ds.time) == 3
    assert "T" not in ds
    assert "Temperature" in ds


def test_rename_var():
    ds = xncml.open_ncml(data / "renameVar.xml")
    assert ds.attrs["title"] == "Example Data"

    assert "ReletiveHumidity" in ds
    assert all(ds.lat.data == [41.0, 40.0, 39.0])
    assert all(ds.lon.data == [-109.0, -107.0, -105.0, -103.0])
    assert ds.lon.dtype == np.float32
    assert all(ds.time.data == [6, 18, 24, 36])
    assert ds.time.dtype == np.int32

    assert all(np.equal(ds.attrs["testFloat"], [1.0, 2.0, 3.0, 4.0]))

    assert ds.attrs["testByte"][0].dtype == np.int8
    assert ds.attrs["testShort"][0].dtype == np.int16
    assert ds.attrs["testInt"][0].dtype == np.int32
    assert ds.attrs["testFloat"][0].dtype == np.float32
    assert ds.attrs["testDouble"][0].dtype == np.float64


def test_agg_union_simple():
    ds = xncml.open_ncml(data / "aggUnionSimple.xml")
    assert ds.attrs["title"] == "Union cldc and lflx"
    assert len(ds.lat) == 21
    assert ds.lat.attrs["units"] == "degrees_north"
    assert all(ds.lat.data[:3] == [10, 9, 8])
    assert len(ds.time) == 456
    assert "lflx" in ds
    assert "cldc" in ds
    assert ds.lflx.shape == (456, 21, 360)


def test_agg_union():
    ds = xncml.open_ncml(data / "aggUnion.xml")
    assert ds.attrs["title"] == "Example Data"
    assert ds.lat.size == 3
    assert ds.time.size == 2
    assert ds.ReletiveHumidity.shape == (2, 3, 4)
    assert ds.ReletiveHumidity.attrs["units"] == "percent"
    assert ds.Temperature.shape == (2, 3, 4)
    assert ds.Temperature.attrs["units"] == "degC"


def test_agg_union_rename():
    ds = xncml.open_ncml(data / "aggUnionRename.xml")
    assert "LavaFlow" in ds.variables


def test_agg_union_scan():
    ds = xncml.open_ncml(data / "aggUnionScan.xml")
    assert "lflx" in ds
    assert "cldc" in ds


def test_read():
    ds = xncml.open_ncml(data / "testRead.xml")
    assert ds.attrs["title"] == "Example Data"
    assert ds.attrs["testFloat"] == (1.0, 2.0, 3.0, 4.0)


def test_read_override():
    ds = xncml.open_ncml(data / "testReadOverride.xml")
    assert "rh" not in ds.variables


@pytest.mark.skip(reason="unclear if this is meant to fail")
def test_read_https():
    ds = xncml.open_ncml(data / "testReadHttps.xml")
    assert ds.attrs["title"] == "Example Data"


def test_agg_existing_inequivalent_cals():
    ds = xncml.open_ncml(data / "agg_with_calendar/aggExistingInequivalentCals.xml")
    assert ds.time.size == 725
    assert ds.time[-1] == dt.datetime(2018, 12, 31)


@pytest.mark.skip(reason="dateFormatMark not implemented")
def test_aggexistingone():
    ds = xncml.open_ncml(data / "aggExistingOne.ncml")
    assert len(ds.time) == 3


@pytest.mark.skip(reason="dateFormatMark not implemented")
@pytest.mark.skip(reason="<promoteGlobalAttribute> not implemented")
def test_agg_existing_promote():
    ds = xncml.open_ncml(data / "aggExistingPromote.ncml")
    assert "times" in ds.variables


@pytest.mark.skip(reason="<promoteGlobalAttribute> not implemented")
def test_agg_existing_promote2():
    ds = xncml.open_ncml(data / "aggExistingPromote2.ncml")


def test_agg_join_new_scalar_coord():
    ds = xncml.open_ncml(data / "aggJoinNewScalarCoord.xml")
    # TODO: Complete test


def test_exercise_1():
    ds = xncml.open_ncml(data / "exercise1.ncml")
    # TODO: Complete test


def test_read_meta_data():
    ds = xncml.open_ncml(data / "readMetadata.xml")
    assert ds.attrs["title"] == "Example Data"
    assert ds.variables["T"].attrs["units"] == "degC"


# --- #
def check_dimension(ds):
    assert len(ds["lat"]) == 3
    assert len(ds["lon"]) == 4
    assert len(ds["time"]) == 59


def check_coord_var(ds):
    lat = ds["lat"]
    assert len(lat) == 3
    assert lat.dtype == np.float32
    assert lat.dims == ("lat",)
    assert lat.attrs["units"] == "degrees_north"
    assert all(lat.data == [41.0, 40.0, 39.0])


def check_agg_coord_var(ds):
    time = ds["time"]
    assert time.dims == ("time",)
    assert len(time) == 59
    assert time.dtype == np.int32


def check_read_data(ds):
    t = ds["T"]
    assert t.dims == ("time", "lat", "lon")
    assert t.size == 708
    assert t.shape == (59, 3, 4)
    assert t.dtype == float
    assert "T" in ds.data_vars
