"""Integration tests for the imagery tile coordinate workflow.

These tests exercise the coordinate conversion functions in
`pyseas.imagery.tiles`, verifying that bounding boxes and tile edges
remain consistent across the workflow.
"""

import pytest


def test_tile_coordinate_workflow_covers_extent():
    """Verify that tile edges computed from bbox coordinates cover the input extent."""
    pytest.importorskip("osgeo")
    from pyseas.imagery.tiles import bbox_and_zoom_to_xy, tile_edges

    lon_min, lon_max, lat_min, lat_max = -20.0, 20.0, -10.0, 10.0
    zoom = 3

    x_min, x_max, y_min, y_max = bbox_and_zoom_to_xy(lon_min, lon_max, lat_min, lat_max, zoom)
    assert x_min <= x_max
    assert y_min <= y_max

    west, south, east, north = tile_edges(x_min, y_max, zoom)
    assert west <= lon_min
    assert east >= lon_max
    assert south <= lat_min
    assert north >= lat_max


def test_tile_downloader_check_tile_count_integration():
    """Verify TileDownloader integration with tile range computation."""
    pytest.importorskip("osgeo")
    from pyseas.imagery.tiles import TileDownloader

    downloader = TileDownloader("http://example.com/{x}/{y}/{z}.png", max_tiles=10)

    x_min, x_max, y_min, y_max = 0, 2, 0, 2
    assert downloader.check_tile_count(x_min, x_max, y_min, y_max) == 9

    with pytest.raises(ValueError):
        downloader.check_tile_count(0, 4, 0, 1)
