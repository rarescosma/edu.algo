#!/usr/bin/env python3
"""
Probably extremely suboptimal implementation of
Karger's minimum cut algorithm for undirected graphs.
"""
import math
import random
from copy import deepcopy
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import Dict, Generator, List, Set, Tuple

from more_itertools import grouper

Vertex = int
Adjacency = Set[Vertex]
AdjacencyRow = List[Vertex]
Edge = Tuple[Vertex, Vertex]


class Graph:
    graph: Dict[Vertex, Adjacency]
    _orig: Dict[Vertex, Adjacency]
    max_node: int

    def __init__(self, graph: Dict[Vertex, Adjacency]) -> None:
        self.graph = graph
        self._orig = deepcopy(graph)
        self.max_node = max(graph.keys())

    def _supernode(self) -> Generator[int, None, None]:
        a = self.max_node + 1
        while True:
            yield a
            a = a + 1

    @classmethod
    def from_adjacency_list(cls, adj_l: List[AdjacencyRow]) -> "Graph":
        _graph = {}
        for row in adj_l:
            vertex, *edges = row
            _graph[vertex] = set(edges)
        return cls(_graph)

    def search_min_cut(self) -> int:
        super_gen = self._supernode()
        contractions = {}

        while len(self.graph) > 2:
            u, v = self.select_random_edge()
            super_v = next(super_gen)
            contractions[super_v] = (u, v)

            # supervertex gobbles all adjacencies
            for vertex, edges in self.graph.items():
                if u in edges or v in edges:
                    self.graph[vertex].add(super_v)
                    self.graph[vertex] -= {u, v}

            self.graph[super_v] = (self.graph[u] | self.graph[v]) - {
                u,
                v,
                super_v,
            }

            # get rid of u, v
            self.graph.pop(u)
            self.graph.pop(v)

        x, y = list(self.graph.keys())[:2]
        _expander = partial(
            _expand_node, contractions, set(contractions.keys())
        )
        xs, ys = _expander({x}), _expander({y})
        assert not xs & ys

        # count edges between xs and ys
        cut_edges = {
            _make_edge(_x, _y)
            for _x in xs
            for _y in (self._orig[_x] & ys)
            if _x != _y
        }
        return len(cut_edges)

    def select_random_edge(self) -> Edge:
        u, v = random.sample(self.graph.keys(), k=2)
        return u, v


def _make_edge(x: Vertex, y: Vertex) -> Edge:
    return (x, y) if x < y else (y, x)


def _expand_node(
    contractions: Dict[Vertex, List[Vertex]],
    c_keys: Set[Vertex],
    xs: Set[Vertex],
) -> Set[Vertex]:
    expandable = xs & c_keys
    if not expandable:
        return xs

    primal = xs - c_keys
    expanded = _expand_node(
        contractions,
        c_keys,
        {i for o in expandable for i in contractions[o]},
    )
    return expanded | primal


def _compute(adj_l: List[AdjacencyRow], _: int) -> int:
    return Graph.from_adjacency_list(adj_l).search_min_cut()


if __name__ == "__main__":
    lines = [
        _
        for _ in (Path(__file__).parent / "../../data/min_cut.txt")
        .read_text()
        .splitlines()
        if _
    ]
    _adj_l = [[int(_) for _ in line.split()] for line in lines]

    _n = len(_adj_l)
    _num_tries, _done, _min = math.ceil(_n * _n * math.log(_n)), 0, math.inf
    _computer = partial(_compute, _adj_l)

    for _chunk in grouper(range(0, _num_tries), 1000):
        with Pool() as pool:
            _cuts = pool.map(_computer, _chunk)
            _min = min(min(_cuts), _min)
            _done += len(_chunk)
            print(f"after {_done} iterations, min cut is {_min}")
