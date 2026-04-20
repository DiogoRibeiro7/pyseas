"""Unit tests for pyseas.imagery.tiles helper functions.

Some tests require the osgeo package and will be skipped if it is not
available in the environment.
"""

import pytest


def test_tile_downloader_tile_count():
    """Ensure tile count validation raises when the requested tile count is too high."""
    pytest.importorskip("osgeo")
    from pyseas.imagery.tiles import TileDownloader

    downloader = TileDownloader("http://example.com/{x}/{y}/{z}.png", max_tiles=4)
    assert downloader.check_tile_count(0, 1, 0, 1) == 4

    with pytest.raises(ValueError):
        downloader.check_tile_count(0, 2, 0, 1)


def test_tile_edge_conversions():
    """Verify tile coordinate conversion functions produce expected lat/lon bounds."""
    pytest.importorskip("osgeo")
    from pyseas.imagery.tiles import tile_edges, x_to_lon_edges, y_to_lat_edges

    lon1, lon2 = x_to_lon_edges(0, 1)
    assert lon1 == -180
    assert lon2 == 0

    lat1, lat2 = y_to_lat_edges(0, 1)
    assert lat1 > lat2
    assert -90 <= lat2 < lat1 <= 90

    edges = tile_edges(1, 1, 1)
    assert edges[0] == 0
    assert edges[2] == 180
    assert edges[1] > edges[3]
