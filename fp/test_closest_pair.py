"""Tests for closest_pair."""
from operator import itemgetter

import pytest
from hypothesis import given
from hypothesis.strategies import floats, lists, tuples

from .closest_pair import Point, _distance, brute, closest_pair


@given(
    lists(
        tuples(
            floats(allow_nan=False, max_value=10000, min_value=-10000),
            floats(allow_nan=False, max_value=10000, min_value=-10000),
        ),
        min_size=32,
        unique_by=(itemgetter(0), itemgetter(1)),
    )
)
def test_closest_pair(xys: list[tuple[float, float]]) -> None:
    pts = [Point(*_) for _ in xys]

    assert _distance(closest_pair(pts)) == pytest.approx(_distance(brute(pts)))
