"""Unit tests covering dnc + MergeSort."""
import random
from multiprocessing import Pool as ProcPool
from multiprocessing.dummy import Pool
from time import time
from typing import List

import pytest
from hypothesis import given
from hypothesis.strategies import floats, integers, lists, one_of, text

from .dnc import divide_and_conquer
from .merge_sort import MergeSort


@given(
    one_of(
        lists(integers(), max_size=1024),
        lists(floats(allow_nan=False)),
        lists(text()),
    )
)
def test_merge_sort(input_arr: list) -> None:
    s_lists = [MergeSort.pure(_) for _ in input_arr]
    _sorted = divide_and_conquer(s_lists)
    if _sorted:
        assert _sorted[0].values == sorted(input_arr[:])


@given(
    one_of(
        lists(integers(), max_size=1024),
        lists(floats(allow_nan=False)),
        lists(text()),
    )
)
def test_parallel_merge_sort(input_arr: list) -> None:
    s_lists = [MergeSort.pure(_) for _ in input_arr]
    with Pool() as pool:
        _sorted = divide_and_conquer(s_lists, starmap=pool.starmap)
        if _sorted:
            assert _sorted[0].values == sorted(input_arr[:])


@given(lists(integers()))
def test_sortlist(input_arr: List[int]) -> None:
    _pivot = len(input_arr) // 2
    a, b = sorted(input_arr[:_pivot]), sorted(input_arr[_pivot:])

    left, right = MergeSort(a), MergeSort(b)

    assert (left + right).values == sorted([*a, *b])


@pytest.mark.bench
def test_speedup() -> None:
    _size = 200
    input_arr = random.sample(range(1, 100000000), _size)
    input_s = [MergeSort.pure(_) for _ in input_arr]

    start_time = time()
    divide_and_conquer(input_s)
    print(f"Normal dnc starmap time: {time() - start_time}")

    start_time = time()
    with ProcPool(12) as pool:
        divide_and_conquer(input_s, starmap=pool.starmap)
    print(f"Pool dnc starmap time: {time() - start_time}")
