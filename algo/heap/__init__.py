"""Generic heap."""
import abc
from dataclasses import dataclass
from typing import Any, Generic, Iterable, List, Protocol, Tuple, TypeVar, Union


class SupportsLessThanEq(Protocol):
    def __le__(self, __other: Any) -> bool:
        ...


class Keyed(Protocol):
    @property
    @abc.abstractmethod
    def key(self) -> SupportsLessThanEq:
        ...


X = TypeVar("X", bound=Keyed)


@dataclass
class Heap(Generic[X]):
    _arr: list[X]

    @classmethod
    def from_iterable(cls, xs: Iterable[X]) -> "Heap[X]":
        _it = iter(xs)
        root = cls(_arr=[next(_it)])
        for x in _it:
            root.insert(x)
        return root

    @classmethod
    def from_raw(cls, xs: list[X]) -> "Heap[X]":
        return cls(_arr=xs[:])

    def __bool__(self) -> bool:
        return bool(self._arr)

    @staticmethod
    def parent(i: int) -> int:
        _res = i >> 1
        return _res if i % 2 else _res - 1

    @staticmethod
    def children(i: int) -> Tuple[int, int]:
        _db = (i + 1) << 1
        return _db - 1, _db

    def insert(self, x: X) -> None:
        _next_leaf = len(self._arr)
        self._arr.append(x)

        # Keep heap invariant -> bubble-up
        self._bubble_up(_next_leaf)

    def extract_min(self) -> X:
        self._swap(0, -1)
        root = self._arr.pop()
        self._bubble_down()
        return root

    def delete(self, x: X) -> None:
        _ind, _last = self._arr.index(x), self._arr[-1]
        self._swap(_ind, -1)
        self._arr.pop()

        _parent = self.parent(_ind)
        if _last.key <= self._arr[_parent].key:
            self._bubble_up(_ind)
        else:
            self._bubble_down(_ind)

    def _bubble_up(self, leaf: int, up_to: int = 0) -> None:
        # we've reached the root
        if leaf == up_to:
            return

        _parent = self.parent(leaf)
        arr = self._arr
        if arr[_parent].key <= arr[leaf].key:
            return

        # swap and re-check
        self._swap(leaf, _parent)
        self._bubble_up(_parent)

    def _bubble_down(self, down_from: int = 0) -> None:
        # we've reached a leaf
        if not (_children := self._children(down_from)):
            return

        # swap with smallest child
        arr = self._arr
        if (
            len(_children) == 2
            and arr[_children[1]].key <= arr[_children[0]].key
        ):
            swap_with = _children[1]
        else:
            swap_with = _children[0]

        if arr[down_from].key <= arr[swap_with].key:
            return

        # swap and re-check
        self._swap(down_from, swap_with)
        self._bubble_down(swap_with)

    def _swap(self, i: int, j: int) -> None:
        self._arr[i], self._arr[j] = self._arr[j], self._arr[i]

    def _children(self, i: int) -> List[int]:
        return [_ for _ in self.children(i) if _ < len(self._arr)]

    def as_dict(self, i: int = 0) -> Union[dict, X]:
        _children = self._children(i)
        _val = self._arr[i]
        if not _children:
            return _val
        return {_val: list(map(self.as_dict, _children))}
