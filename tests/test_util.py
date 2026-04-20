"""Unit tests for the pyseas.util helper functions.

This module verifies array conversion, longitude averaging, and sorting
utility behavior.
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pyseas import util


def test_asarray_converts_lists_and_series():
    """Verify that asarray converts both Python lists and pandas Series."""
    data_list = [1, 2, 3]
    data_series = pd.Series([4, 5, 6])

    assert np.array_equal(util.asarray(data_list), np.array([1, 2, 3]))
    assert np.array_equal(util.asarray(data_series), np.array([4, 5, 6]))


def test_asarray_applies_dtype():
    """Verify that asarray respects the requested numpy dtype."""
    result = util.asarray([1, 2, 3], dtype=float)
    assert result.dtype == float
    assert np.array_equal(result, np.array([1.0, 2.0, 3.0]))


def test_lon_avg_wraps_around_dateline():
    """Verify longitude averaging correctly handles dateline wrap-around."""
    longitudes = np.array([170.0, -170.0])
    average = util.lon_avg(longitudes)
    assert np.isclose(average, 180.0, atol=1e-6) or np.isclose(
        average, -180.0, atol=1e-6
    )


def test_is_sorted_with_sorted_and_unsorted_sequences():
    """Verify that is_sorted returns True for sorted sequences and False otherwise."""
    assert util.is_sorted([1, 2, 3, 4]) is True
    assert util.is_sorted([1, 1, 2, 2]) is True
    assert util.is_sorted([1, 3, 2, 4]) is False
    assert util.is_sorted([]) is True
    assert util.is_sorted([42]) is True
