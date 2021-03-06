"""Tests for select_second."""
from hypothesis import given
from hypothesis.strategies import integers, lists

from .select_second import second_largest


@given(lists(integers(), min_size=64, max_size=64, unique=True))
def test_select_second(ints: list[int]) -> None:
    assert second_largest(ints) == sorted(ints)[-2]
