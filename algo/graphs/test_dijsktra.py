"""Tests for dijkstra."""
from collections import defaultdict
from pathlib import Path

import pytest

from .dijkstra import Edge, Graph, dijsktra_heap, dijsktra_naive


@pytest.mark.wip
def test_dijsktra() -> None:
    rows = [
        _.split()
        for _ in (Path(__file__).parent / "../../data/dijsktra.txt")
        .read_text()
        .splitlines()
        if _
    ]

    _graph: Graph = defaultdict(list)
    for head, *edges in rows:
        _head = int(head)
        _graph[_head] = [Edge(_head, *map(int, _.split(","))) for _ in edges]

    dists = dijsktra_heap(_graph, 1)
    dists_naive, _ = dijsktra_naive(_graph, 1)
    assert dists == dists_naive

    keys = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    _expected = [2599, 2610, 2947, 2052, 2367, 2399, 2029, 2442, 2505, 3068]
    assert [dists[k] for k in keys] == _expected
