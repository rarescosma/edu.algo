"""Depth-first graph exploration primitive.
"""
from collections import deque
from enum import Enum, auto
from typing import NamedTuple

from devtools import debug

from ._types import Graph, X

current_label: int


class TaskType(Enum):
    FIN = auto()
    EXP = auto()


class Task(NamedTuple):
    v_name: X
    kind: TaskType


def dfs(g: Graph, s_name: X) -> None:
    s = v = g.vertices[s_name]
    s.explored = True
    topo = len(g.vertices)

    q = deque([Task(s_name, TaskType.FIN), Task(s_name, TaskType.EXP)])
    while True:
        unexplored = [_ for _ in g.edges[v.name] if not g.vertices[_].explored]
        if unexplored:
            v = g.vertices[unexplored[0]]
            v.explored = True
            q.extend([Task(v.name, TaskType.FIN), Task(v.name, TaskType.EXP)])
            continue
        if not q:
            break
        task = q.pop()
        if task.kind == TaskType.FIN:
            g.vertices[task.v_name].topo = topo
            topo -= 1
        elif task.kind == TaskType.EXP:
            v = g.vertices[task.v_name]


def rec_dfs(g: Graph, s_name: X, outer: bool = False) -> None:
    global current_label
    if outer:
        current_label = len(g.vertices)

    s = g.vertices[s_name]
    s.explored = True
    for v_name in g.edges[s_name]:
        if not g.vertices[v_name].explored:
            rec_dfs(g, v_name)

    s.topo = current_label
    current_label -= 1


def topo_ord(g: Graph) -> None:
    for v in g.vertices.values():
        if not v.explored:
            dfs(g, v.name)


if __name__ == "__main__":
    _ = """
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
    print(">> stack-based:")
    _graph = Graph.from_adj_l(_adj_l)
    dfs(_graph, "s")
    debug(_graph.vertices)

    print("\n>> recursion-based:")
    _graph = Graph.from_adj_l(_adj_l)
    rec_dfs(_graph, "s", True)
    debug(_graph.vertices)
