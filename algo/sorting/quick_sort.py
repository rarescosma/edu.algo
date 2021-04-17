#!/usr/bin/env python3
"""
QuickSort - we receive two sub-arrays from the recursive step,
call partition on them and glue them together.
"""
import abc
from pathlib import Path
from random import randrange
from typing import Any, List, Protocol, Type, TypeVar


class SupportsLessThan(Protocol):
    def __lt__(self, __other: Any) -> bool:
        ...


X = TypeVar("X", bound=SupportsLessThan)

total_comps = 0


class Strategy(metaclass=abc.ABCMeta):
    @staticmethod
    def choose_pivot(start: int, end: int, xs: List[X]) -> int:
        """Return a pivot index given the array bounds and the array."""


class MedianOfThree(Strategy):
    @staticmethod
    def choose_pivot(start: int, end: int, xs: List[X]) -> int:
        i, k = start, end - 1
        if (len_xs := len(xs)) % 2 == 1:  # odd array
            j = len_xs // 2
        else:  # even array
            j = len_xs // 2 - 1
        mid_val = sorted([xs[i], xs[j], xs[k]])[1]
        if mid_val == xs[i]:
            return i
        if mid_val == xs[k]:
            return k
        return j


class Random(Strategy):
    @staticmethod
    def choose_pivot(start: int, end: int, xs: List[X]) -> int:
        return randrange(start, end)


class First(Strategy):
    @staticmethod
    def choose_pivot(start: int, end: int, xs: List[X]) -> int:
        return start


class Last(Strategy):
    @staticmethod
    def choose_pivot(start: int, end: int, xs: List[X]) -> int:
        return end - 1


def quicksort(xs: List[X], strategy: Type[Strategy] = MedianOfThree) -> None:
    return _quicksort(xs, 0, len(xs), strategy=strategy)


def _quicksort(
    xs: List[X], start: int, end: int, strategy: Type[Strategy]
) -> None:
    global total_comps  # pylint:disable=global-statement)
    len_xs = len(xs[start:end])

    if len_xs <= 1:
        return

    # pivot choosing
    p_i = strategy.choose_pivot(start, end, xs)
    _swap(xs, start, p_i)  # pivot is now first element

    p_f = _partition(xs, start, end)
    _swap(xs, p_f, start)

    _quicksort(xs, start, p_f, strategy=strategy)
    total_comps = total_comps + (p_f - start)
    _quicksort(xs, p_f + 1, end, strategy=strategy)
    total_comps = total_comps + (end - (p_f + 1))


def _swap(xs: List[X], a: int, b: int) -> None:
    """In-place, mutating(!) swap a'th and b'th elements of xs."""
    xs[a], xs[b] = xs[b], xs[a]


def _partition(xs: List[X], start: int, end: int) -> int:
    i, j, pivot = start + 1, start + 1, xs[start]
    while j < end:
        if xs[j] < pivot:
            _swap(xs, j, i)
            i = i + 1
        j = j + 1
    return i - 1


if __name__ == "__main__":
    ints = [
        int(_)
        for _ in (Path(__file__).parent / "../../data/quick_sort.txt")
        .read_text()
        .splitlines()
    ]
    quicksort(ints, strategy=MedianOfThree)
    print(f"{total_comps=}")
