"""Unit tests covering QuickSort"""
from copy import deepcopy

from hypothesis import given
from hypothesis.strategies import floats, integers, lists, one_of, text

from .quick_sort import quicksort


@given(
    one_of(
        lists(integers(), unique=True, max_size=1024),
        lists(floats(allow_nan=False)),
        lists(text()),
    )
)
def test_quick_sort(input_arr: list) -> None:
    _copy = deepcopy(input_arr)
    quicksort(_copy)
    assert _copy == sorted(input_arr)
