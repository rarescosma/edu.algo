"""Depth-first graph exploration primitive.

TODO: re-implement recursive version in terms of vertex color
TODO: re-implement topological ordering and re-use it in SCC implementation
TODO: tests
"""
from collections import defaultdict, deque
from pathlib import Path
from typing import Deque, Dict, List, Optional

from devtools import debug

from ._types import Color, Graph, X


def dfs(
    g: Graph,
    s_name: X,
    leader: Optional[X] = None,
    return_fin: bool = False,
) -> List[X]:
    q = deque([s_name])
    fin: List[X] = list()
    while q:
        v = g.vertices[q[-1]]
        if v.seen:
            q.pop()
            if v.color == Color.GRAY and return_fin:
                fin.append(v.name)
                v.color = Color.BLACK
        else:
            v.color = Color.GRAY
            v.leader = leader
            for w_name in g.edges[v.name]:
                if not g.vertices[w_name].seen:
                    q.append(w_name)
    return fin


def topo_ord(g: Graph) -> Deque[X]:
    """Return the node names of G in their topological ordering."""
    q = deque()
    for v in g.vertices.values():
        if not v.seen:
            q.extend(dfs(g, v.name, return_fin=True))
    return q


def find_sccs(
    g: Graph, g_rev: Graph, top_k: Optional[int] = None
) -> Dict[X, int]:
    _topo_ord = topo_ord(g_rev)

    while _topo_ord:
        v = g.vertices[_topo_ord.pop()]
        if not v.seen:
            dfs(g, v.name, leader=v.name)

    sccs = defaultdict(int)
    for v in g.vertices.values():
        assert v.leader is not None
        sccs[v.leader] += 1

    if top_k is None:
        return sccs
    return {_: sccs[_] for _ in sorted(sccs, key=sccs.get)[:top_k]}


if __name__ == "__main__":
    lines = [
        _
        for _ in (Path(__file__).parent / "../../data/scc_small.txt")
        .read_text()
        .splitlines()
        if _
    ]
    edges = [tuple(int(_) for _ in line.split()) for line in lines]
    _g, _g_rev = Graph[int].from_edges(edges)
    debug(find_sccs(_g_rev, _g))
