import pytest

from fp.graphs._types import Graph

EXPECTED_SCCS = [434821, 968, 459, 313, 211]


@pytest.fixture
def simple_digraph():
    """
    a -> c -> e
    ^    ^    ^
    |    |    |
    s -> b -> d
    """
    _adj_l = [
        ["s", "a", "b"],
        ["a", "c"],
        ["b", "c", "d"],
        ["c", "e"],
        ["d", "e"],
        ["e"],
    ]
    return Graph.from_adj_l(_adj_l)
