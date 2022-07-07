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


def test_aggexistingwcoords():
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
    assert all(ds["time"].data == list(range(7, 125,2)))


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


def test_type2():
    ds = xncml.open_ncml(data / "aggExisting2.xml")
    assert ds["time"].attrs["units"] == "hours since 2006-06-16 00:00"
    assert ds["time"].dtype == float
    assert all(ds["time"].data == [12., 13., 14.])


def test_type4():
    ds = xncml.open_ncml(data / "aggExisting4.ncml")
    assert all(ds["time"].data == [1.1496816E9, 1.1496852E9, 1.1496888E9])


def test_type5():
    ds = xncml.open_ncml(data / "aggExisting5.ncml")
    assert ds["time"].dtype == np.int32
    assert all(ds["time"].data == list(range(59)))


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
    assert all(ds["deltaLat"].data == [.1, .1, .01])
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
    assert all(ds.time == ["2005-11-22 22:19:53Z", "2005-11-22 23:19:53Z", "2005-11-23 00:19:59Z"])


def test_agg_synthetic():
    ds = xncml.open_ncml(data / "aggSynthetic.xml")
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
    assert all(ds.lat.data == [41., 40., 39.])
    assert all(ds.lon.data == [-109.0, -107.0, -105.0, -103.0])
    assert ds.lon.dtype == np.float32
    assert (all(ds.time.data == [6, 18, 24, 36]))
    assert ds.time.dtype == np.int32

    assert all(np.equal(ds.attrs["testFloat"], [1., 2., 3., 4.]))

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


def test_read():
    ds = xncml.open_ncml(data / "testRead.xml")


def test_agg_existing_inequivalent_cals():
    ds = xncml.open_ncml(data / "agg_with_calendar/aggExistingInequivalentCals.xml")
    assert ds.time.size == 725
    assert ds.time[-1] == dt.datetime(2018, 12, 31)


@pytest.mark.skip(reason="dateFormatMark not implemented")
def test_aggexistingone():
    ds = xncml.open_ncml(data / "aggExistingOne.ncml")
    assert len(ds.time) == 3


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
    assert all(lat.data == [41., 40., 39.])


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






