"""Karatsuba multiplication."""
from typing import Tuple


def _split_at(x: str, at: int) -> Tuple[int, int]:
    return int(x[:at]), int(x[at:])


def karatsuba_mul(x: int, y: int) -> int:
    """Sneaky Karatsuba."""

    if x < 10 or y < 10:
        return x * y

    # calculate the size of the numbers
    s_x, s_y = str(x), str(y)
    M = max(len(s_x), len(s_y))
    s_x, s_y = s_x.zfill(M), s_y.zfill(M)

    # magic
    j = M // 2
    m2 = M - j

    # split the digit sequences in the middle
    high1, low1 = _split_at(s_x, j)
    high2, low2 = _split_at(s_y, j)

    # 3 recursive calls for numbers approximately half the size
    z0 = karatsuba_mul(low1, low2)
    z1 = karatsuba_mul((low1 + high1), (low2 + high2))
    z2 = karatsuba_mul(high1, high2)

    return z2 * pow(10, (m2 * 2)) + (z1 - z2 - z0) * pow(10, m2) + z0
