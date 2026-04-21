"""Unit tests for pyseas.maps.rasters.

These tests validate rasterization logic and cover origin handling,
extent filling, and per-square-kilometer scaling.
"""

import importlib.util
import pathlib

import numpy as np
import pandas as pd
import pytest

rasters_path = pathlib.Path(__file__).resolve().parents[1] / "pyseas" / "maps" / "rasters.py"
spec = importlib.util.spec_from_file_location("pyseas_maps_rasters", rasters_path)
rasters = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rasters)


def test_uniform():
    """Ensure df2raster returns uniformly scaled values for a gridded dataset."""
    scale = 4
    lon_bin_template = np.arange(-180 * scale, 180 * scale)
    lat_bin_template = np.arange(-90 * scale, 90 * scale)
    lon_bin, lat_bin = [
        x.flatten() for x in np.meshgrid(lon_bin_template, lat_bin_template, indexing="ij")
    ]
    km_per_deg = 111
    values = np.cos(np.radians(lat_bin / scale)) / (scale**2) * (km_per_deg**2)
    df = pd.DataFrame({"lon_bin": lon_bin, "lat_bin": lat_bin, "values": values})
    raster = rasters.df2raster(
        df, "lon_bin", "lat_bin", "values", xyscale=scale, origin="lower", per_km2=True
    )
    expected = (km_per_deg**2) / (rasters.KM_PER_DEG_LAT * rasters.KM_PER_DEG_LON0)
    assert np.allclose(raster, expected, atol=0.001)


def test_df2raster_invalid_origin():
    """Verify that invalid origin values raise a ValueError."""
    df = pd.DataFrame({"lon_bin": [0], "lat_bin": [0], "values": [1]})
    with pytest.raises(ValueError, match="origin must be 'upper' or 'lower'"):
        rasters.df2raster(df, "lon_bin", "lat_bin", "values", xyscale=1, origin="middle")


def test_df2raster_fill_and_extent():
    """Verify fill behavior and extent handling for df2raster outputs."""
    df = pd.DataFrame({"lon_bin": [0, 1], "lat_bin": [0, 1], "values": [10, 20]})
    raster = rasters.df2raster(
        df,
        "lon_bin",
        "lat_bin",
        "values",
        xyscale=1,
        extent=(0, 2, 0, 2),
        origin="upper",
        fill=-1,
    )

    expected = np.array([[-1.0, 20.0], [10.0, -1.0]])
    assert np.array_equal(raster, expected)


def test_df2raster_per_km2_scaling():
    """Verify per-km2 scaling uses latitude-dependent area correction."""
    df = pd.DataFrame({"lon_bin": [0], "lat_bin": [0], "values": [1.0]})
    raster = rasters.df2raster(
        df,
        "lon_bin",
        "lat_bin",
        "values",
        xyscale=1,
        extent=(0, 1, 0, 1),
        origin="lower",
        per_km2=True,
        fill=0.0,
    )

    expected = 1.0 / (
        np.cos(np.radians(0.0)) * (rasters.KM_PER_DEG_LAT * rasters.KM_PER_DEG_LON0 / 1.0**2)
    )
    assert raster.shape == (1, 1)
    assert np.isclose(raster[0, 0], expected)
