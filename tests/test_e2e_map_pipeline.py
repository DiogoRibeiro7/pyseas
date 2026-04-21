"""End-to-end tests for a basic pyseas map generation workflow."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest


def test_end_to_end_map_generation():
    """Validate a full workflow from data frame through raster to map image."""
    pytest.importorskip("cartopy")
    from pyseas import maps

    lon_values = np.array([-3.0, 0.0, 3.0])
    lat_values = np.array([-2.0, 0.0, 2.0])
    values = np.array([1.0, 2.0, 3.0])

    df = pd.DataFrame(
        {
            "lon_bin": lon_values.astype(int),
            "lat_bin": lat_values.astype(int),
            "values": values,
        }
    )

    raster = maps.rasters.df2raster(
        df,
        "lon_bin",
        "lat_bin",
        "values",
        xyscale=1,
        extent=(-5, 5, -5, 5),
        origin="lower",
        fill=0.0,
    )

    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(1, 1, 1, projection=maps.core.identity)
    image = maps.core.add_raster(
        raster,
        ax=ax,
        extent=(-5, 5, -5, 5),
        origin="lower",
        cmap=plt.cm.inferno,
    )

    fig.canvas.draw()
    assert image is not None
    assert ax.images and ax.images[-1] is image
    assert image.get_array().shape == raster.shape
    assert np.nanmax(image.get_array()) == pytest.approx(3.0)
    plt.close(fig)
