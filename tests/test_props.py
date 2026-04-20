"""Unit tests for the pyseas.props module.

These tests cover Props object construction, representation, and default
style properties loading.
"""

import pytest

from pyseas import props


def test_props_repr_small():
    """Verify that small Props instances use a compact repr format."""
    p = props.Props(color="red", width=5)
    assert p.color == "red"
    assert p.width == 5
    assert "Props(" in repr(p)
    assert "color='red'" in repr(p)


def test_props_repr_large():
    """Verify that larger Props instances format repr with line breaks."""
    p = props.Props(a=1, b=2, c=3, d=4)
    assert isinstance(repr(p), str)
    assert repr(p).startswith("Props(\n")


def test_props_numeric_key_name():
    """Verify that numeric keys are converted to valid Python attribute names."""
    p = props.Props(**{"1color": "blue"})
    assert hasattr(p, "_1color")
    assert getattr(p, "_1color") == "blue"


def test_default_props_are_loaded():
    """Verify that default theme properties are loaded from the JSON source."""
    assert isinstance(props.dark, props.Props)
    assert isinstance(props.light, props.Props)
    assert props.dark.land.color == "#374a6d"
    assert props.light.ocean.color == "#FFFFFF"
    assert props.fishing.fishing.width == 1.0
    assert list(props.chart.colors.__dict__.keys())
