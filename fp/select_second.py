"""An interesting solution to the 2nd item selection problem."""
from collections import defaultdict
from typing import Iterable, Tuple


def second_largest(xs: list[int]) -> int:
    assert _is_2_pow((len_xs := len(xs))), "input size is not a power of 2"

    losers = defaultdict(list)
    players = list(range(len_xs))

    # N - 1 pairwise comparisons in total
    while len(players) > 1:
        new_players = []
        for i, j in _pairs(players):
            winner, loser = (i, j) if xs[i] > xs[j] else (j, i)
            new_players.append(winner)
            losers[winner].append(loser)
        players = new_players

    # winner has been compared to at most log(N) losers
    # => it will take at most another log(N) - 1 comparisons
    # to find the silver medal
    winner = players[0]
    return max(xs[_] for _ in losers[winner])


def _is_2_pow(x: int) -> bool:
    # lolwhat
    return (x & (x - 1) == 0) and x != 0


def _pairs(xs: list[int]) -> Iterable[Tuple[int, int]]:
    for _ in range(0, len(xs), 2):
        yield xs[_], xs[_ + 1]
