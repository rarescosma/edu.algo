"""Unit tests covering InvCount."""
from hypothesis import given
from hypothesis.strategies import integers, lists

from fp.dnc import divide_and_conquer
from fp.inv_count import InvCount


def _brute(arr: list) -> int:
    n = len(arr)
    inv_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inv_count += 1

    return inv_count


def test_textbook_case() -> None:
    xs = [1, 3, 5, 2, 4, 6]
    ys = [InvCount.pure(_) for _ in xs]
    _counted = divide_and_conquer(ys)
    assert len(_counted) == 1
    assert _counted[0].inv_count == 3


@given(lists(integers(), min_size=3))
def test_against_derpy_implementation(xs: list) -> None:
    ys = [InvCount.pure(_) for _ in xs]
    _counted = divide_and_conquer(ys)[0].inv_count
    assert _counted == _brute(xs)
