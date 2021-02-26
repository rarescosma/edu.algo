"""Unit tests covering InvCount."""
from fp.dnc import divide_and_conquer
from fp.inv_count import InvCount


def test_textbook_case() -> None:
    xs = [1, 3, 5, 2, 4, 6]
    ys = [InvCount.pure(_) for _ in xs]
    _counted = divide_and_conquer(ys)
    assert len(_counted) == 1
    assert _counted[0].inv_count == 3
