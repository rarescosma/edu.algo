"""Given a set of points on a plane by their X, Y coordinates,
find the closest pair of points (by their Euclidean distance).
"""
import math
from itertools import permutations
from typing import Iterable, NamedTuple, Sequence, Tuple, cast

from more_itertools import partition


class Point(NamedTuple):
    x: float
    y: float


Points = Sequence[Point]
Pair = Tuple[Point, Point]


def _distance(pair: Pair) -> float:
    return math.dist(*pair)


def _best_of(*pairs: Pair) -> Pair:
    return min(pairs, key=_distance)


def _closest_split_pair(p_y: Points, x_bar: float, delta_pair: Pair) -> Pair:
    # take a strip of width delta around the median X
    delta = _distance(delta_pair)
    s_y = [_ for _ in p_y if abs(_.x - x_bar) <= delta]

    len_s_y, best, best_pair = len(s_y), delta, delta_pair

    # for each point in the strip look at max 7 points
    # ahead (WTF?! - this is where the sparsity proof comes in)
    for i in range(0, len_s_y):
        for j in range(1, min(7, len_s_y - i)):
            pair = s_y[i], s_y[i + j]
            if (d := _distance(pair)) < best:
                best, best_pair = d, pair
    return best_pair


def _closest_pair(p_x: Points, p_y: Points) -> Pair:
    if (len_x := len(p_x)) <= 3 and len(p_y) <= 3:
        return brute({*p_x, *p_y})

    # partition the X-sorted array around median X
    mid = len_x // 2
    q_x, r_x, x_bar = p_x[:mid], p_x[mid:], p_x[mid].x

    # partition the Y-sorted array (around median X again!)
    _qr = partition(lambda _: _.x > x_bar, p_y)
    q_y, r_y = list(_qr[0]), list(_qr[1])

    delta_pair = _best_of(
        _closest_pair(q_x, q_y),
        _closest_pair(r_x, r_y),
    )
    return _closest_split_pair(p_y, x_bar, delta_pair)


def closest_pair(points: Points) -> Pair:
    return _closest_pair(
        sorted(points, key=lambda _: _.x),
        sorted(points, key=lambda _: _.y),
    )


def brute(points: Iterable[Point]) -> Pair:
    return _best_of(*cast(list[Pair], permutations(points, r=2)))
