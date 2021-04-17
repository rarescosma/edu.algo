"""Common models for graph primitives."""
import math
from dataclasses import dataclass
from typing import Dict, Generic, List, Optional, Set, TypeVar
from enum import Enum, auto

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
