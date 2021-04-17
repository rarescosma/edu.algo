"""Common models for graph primitives."""
import math
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Generic, List, Optional, Set, Tuple, TypeVar

X = TypeVar("X")
AdjacencyRow = List[X]


class Color(Enum):
    WHITE = auto()
    GRAY = auto()
    BLACK = auto()


@dataclass
class Vertex(Generic[X]):
    name: X
    color: Color = Color.WHITE
    dist: float = math.inf
    leader: Optional[X] = None

    @property
    def seen(self) -> bool:
        return self.color != Color.WHITE


Adjacency = Set[Vertex]


@dataclass
class Graph(Generic[X]):
    vertices: Dict[X, Vertex[X]]
    edges: Dict[X, Set[X]]

    @classmethod
    def from_adj_l(cls, adj_l: List[AdjacencyRow]) -> "Graph":
        _vertices: Dict[X, Vertex[X]] = {}
        _edges = {}
        for row in adj_l:
            for v_name in row:
                if v_name not in _vertices:
                    _vertices[v_name] = Vertex(name=v_name)
            s, *adj = row
            _edges[s] = set(adj)
        return cls(vertices=_vertices, edges=_edges)

    @classmethod
    def from_edges(cls, edge_l: List[Tuple[X, X]]) -> Tuple["Graph", "Graph"]:
        _vertices: Dict[X, Vertex[X]] = {}
        _edges = defaultdict(set)
        _rev_edges = defaultdict(set)
        for u_name, v_name in edge_l:
            _vertices[u_name] = Vertex(name=u_name)
            _vertices[v_name] = Vertex(name=v_name)
            _edges[u_name].add(v_name)
            _rev_edges[v_name].add(u_name)
        return (
            cls(vertices=_vertices, edges=_edges),
            cls(vertices=deepcopy(_vertices), edges=_rev_edges),
        )
