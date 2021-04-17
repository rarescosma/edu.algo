"""Dijkstra's famous shortest path algorithm for DiGraphs.

The naive implementation looks at all edges on every vertex iteration,
therefore running in O(MN) time.

Using a heap with clever invariants we can achieve a blazing O(M log N)
running time.
"""
import math
from typing import Dict, NamedTuple, Tuple

from algo.heap import Heap

VName = int


class Edge(NamedTuple):
    head: VName
    tail: VName
    dist: float


class Vertex(NamedTuple):
    name: VName
    key: float


Graph = Dict[VName, list[Edge]]
ShortestDists = Dict[VName, float]
ShortestPaths = Dict[VName, list[VName]]


def dijsktra_naive(g: Graph, s: VName) -> Tuple[ShortestDists, ShortestPaths]:
    explored, a = {s}, {s: 0.0}
    b: ShortestPaths = {s: []}

    len_g = len(g)
    while len(explored) != len_g:
        crossing = [
            _edge
            for _v in explored
            for _edge in g[_v]
            if _edge.tail not in explored
        ]
        star = min(crossing, key=lambda _: a[_.head] + _.dist)
        explored.add(star.tail)
        a[star.tail] = a[star.head] + star.dist
        b[star.tail] = [*b[star.head], star.tail]
    return a, b


def dijsktra_heap(g: Graph, s: VName) -> ShortestDists:
    explored, a = {s}, {s: 0.0}

    s_distances = {_.tail: _.dist for _ in g[s]}
    vertices = set(g.keys()) - explored

    _heap = Heap[Vertex].from_iterable(
        (Vertex(_, s_distances.get(_, math.inf)) for _ in vertices)
    )

    while _heap:
        w = _heap.extract_min()
        explored.add(w.name)
        a[w.name] = w.key

        for edge in g[w.name]:
            if edge.tail not in explored:
                old_v = _heap.delete(edge.tail)
                new_v = Vertex(
                    edge.tail,
                    key=min(old_v.key, a[edge.head] + edge.dist),
                )
                _heap.insert(new_v)
    return a
