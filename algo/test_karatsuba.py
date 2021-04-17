"""Unit tests covering Karatsuba multiplication."""
from hypothesis import given
from hypothesis.strategies import integers

from .karatsuba import karatsuba_mul


@given(integers(min_value=1), integers(min_value=1))
def test_karatsuba(x: int, y: int) -> None:
    assert x * y == karatsuba_mul(x, y)
