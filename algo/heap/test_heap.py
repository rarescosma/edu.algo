"""Tests for heap."""
from random import randrange
from typing import NamedTuple

from hypothesis import given
from hypothesis.strategies import integers, lists

from . import Heap


class KInt(NamedTuple):
    key: int

    @property
    def name(self) -> int:
        return self.key


@given(lists(integers(), min_size=8, max_size=128, unique=True))
def test_heap_sort(ints: list[int]) -> None:
    _sorted = sorted(ints)
    heap = Heap[KInt].from_iterable([KInt(_) for _ in ints])

    _mins = list()
    while heap:
        _mins.append(heap.extract_min().key)
    assert _mins == _sorted, f"falsifying: {ints}"


@given(lists(integers(), min_size=8, max_size=128, unique=True))
def test_heap_delete(ints: list[int]) -> None:
    _sorted = sorted(ints)
    heap = Heap[KInt].from_iterable([KInt(_) for _ in ints])

    j = randrange(0, len(ints))
    heap.delete(_sorted.pop(j))

    _mins = list()
    while heap:
        _mins.append(heap.extract_min().key)
    assert _mins == _sorted, f"falsifying: {ints}"
