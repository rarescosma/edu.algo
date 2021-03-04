"""Tests for closest_pair."""
import pytest
from hypothesis import given
from hypothesis.strategies import floats, lists

from .closest_pair import Point, _distance, brute, closest_pair


@given(
    lists(
        floats(
            allow_nan=False,
            allow_infinity=False,
            max_value=10,
            min_value=-10,
        ),
        min_size=100,
        unique=True,
    )
)
def test_closest_pair(coord_space: list[float]) -> None:
    points = [
        Point(coord_space[i], coord_space[i + 1])
        for i in range(0, len(coord_space) - 1, 2)
    ]
    assert _distance(closest_pair(points)) == pytest.approx(
        _distance(brute(points))
    )
