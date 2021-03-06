"""Breadth-first graph exploration primitive.
"""
from collections import deque
from typing import Iterable

from devtools import debug

from ._types import Color, Graph, X


def bfs(g: Graph, s_name: X) -> None:
    s = g.vertices[s_name]
    s.color = Color.BLACK
    s.dist = 0
    s.leader = s_name

    q = deque([s_name])
    while q:
        v = g.vertices[q.popleft()]
        for w_name in g.edges[v.name]:
            if not (w := g.vertices[w_name]).seen:
                w.color = Color.BLACK
                w.dist = v.dist + 1
                w.leader = s_name
                q.append(w_name)


def connected_comps(g: Graph) -> Iterable[Graph]:
    for v in g.vertices.values():
        if not v.seen:
            bfs(g, v.name)

    comps = {_.leader for _ in g.vertices.values()}
    for comp in sorted(comps):
        vertices = {k: v for k, v in g.vertices.items() if v.leader == comp}
        yield Graph(
            vertices=vertices,
            edges={v: adj for v, adj in g.edges.items() if v in vertices},
        )


if __name__ == "__main__":
    _adj_l = [
        ["s", "a", "b"],
        ["a", "s", "c"],
        ["b", "s", "d"],
        ["c", "a", "b", "e"],
        ["d", "b", "e"],
        ["e", "c", "d"],
        ["f"],
    ]
    _graph = Graph.from_adj_l(_adj_l)
    debug(_graph)

    _comps = list(connected_comps(_graph))
    debug(len(_comps))

    assert all(v.seen for v in _graph.vertices.values())
    debug(_comps)
