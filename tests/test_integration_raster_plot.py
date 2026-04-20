"""Integration tests for pyseas raster plotting workflows.

These tests exercise multiple modules together, verifying that data is
converted to a raster and then rendered through the pyseas map pipeline.
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest


def test_df2raster_and_add_raster_integration():
    """Verify that raster conversion and plotting work together."""
    pytest.importorskip("cartopy")
    from pyseas import maps

    df = pd.DataFrame(
        {
            "lon_bin": [0, 1, 0, 1],
            "lat_bin": [0, 0, 1, 1],
            "values": [1, 2, 3, 4],
        }
    )

    raster = maps.rasters.df2raster(
        df,
        "lon_bin",
        "lat_bin",
        "values",
        xyscale=1,
        extent=(0, 2, 0, 2),
        origin="lower",
        fill=np.nan,
    )

    fig, ax = plt.subplots(
        figsize=(4, 3), subplot_kw={"projection": maps.core.identity}
    )
    im = maps.core.add_raster(
        raster,
        ax=ax,
        extent=(0, 2, 0, 2),
        origin="lower",
        cmap=plt.cm.viridis,
    )

    assert im is not None
    assert im.get_array().shape == raster.shape
    assert ax.images and ax.images[-1] is im
    assert pytest.approx(np.nansum(raster), rel=1e-6) == 10.0
    plt.close(fig)
