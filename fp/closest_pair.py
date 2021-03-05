"""Given a set of points on a plane by their X, Y coordinates,
find the closest pair of points (by their Euclidean distance).
"""
import math
from itertools import permutations
from typing import Iterable, NamedTuple, Optional, Sequence, Tuple, cast


# pylint: disable=inherit-non-class
class Point(NamedTuple):
    x: float
    y: float


Pair = Tuple[Point, Point]


def _distance(pair: Pair) -> float:
    """Note: for the sake of our problem we don't need to
    find the actual distance, just the closest pair
    so we can skip taking the square root.
    """
    p, q = pair
    return (p.x - q.x) ** 2 + (p.y - q.y) ** 2


def _best_of(*pairs: Pair) -> Pair:
    return min(pairs, key=_distance)


def _closest_split_pair(
    p_x: Sequence[Point],
    p_y: Sequence[Point],
    delta: float,
) -> Optional[Pair]:
    x_bar = p_x[len(p_x) // 2].x
    s_y = [_ for _ in p_y if abs(_.x - x_bar) <= delta]

    len_s_y, best, best_pair = len(s_y), delta, None

    for i in range(0, len_s_y):
        for j in range(1, min(8, len_s_y - i)):  # friggin' insane!
            pair = s_y[i], s_y[i + j]
            if (d := _distance(pair)) < best:
                best, best_pair = d, pair
    return best_pair


def _closest_pair(p_x: Sequence[Point], p_y: Sequence[Point]) -> Pair:
    if (len_x := len(p_x)) <= 3 and len(p_y) <= 3:
        return brute({*p_x, *p_y})

    # split into left & right halves
    mid = len_x // 2
    q_x, r_x = p_x[:mid], p_x[mid:]

    # gotcha!
    x_mid, q_y, r_y = p_x[mid].x, [], []
    for _ in p_y:
        if _.x <= x_mid:
            q_y.append(_)
        else:
            r_y.append(_)

    delta_pair = _best_of(
        _closest_pair(q_x, q_y),
        _closest_pair(r_x, r_y),
    )
    s_pair = _closest_split_pair(
        p_x,
        p_y,
        delta=math.sqrt(_distance(delta_pair)),
    )
    return delta_pair if s_pair is None else _best_of(delta_pair, s_pair)


def closest_pair(points: Sequence[Point]) -> Pair:
    p_x = sorted(points, key=lambda p: p.x)
    p_y = sorted(points, key=lambda p: p.y)
    return _closest_pair(p_x, p_y)


def brute(points: Iterable[Point]) -> Pair:
    return _best_of(*cast(list[Pair], permutations(points, r=2)))
