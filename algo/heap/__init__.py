"""Generic heap."""
import abc
from dataclasses import dataclass, field
from typing import (
    Any,
    Dict,
    Generic,
    Hashable,
    Iterable,
    List,
    Optional, Protocol,
    Tuple,
    TypeVar,
    Union,
)


class SupportsLessThanEq(Protocol):
    def __le__(self, __other: Any) -> bool:
        ...


class El(Protocol):
    @property
    @abc.abstractmethod
    def name(self) -> Hashable:
        ...

    @property
    @abc.abstractmethod
    def key(self) -> SupportsLessThanEq:
        ...


X = TypeVar("X", bound=El)


@dataclass
class Heap(Generic[X]):
    _arr: list[X] = field(default_factory=list)
    _pos: Dict[Hashable, int] = field(default_factory=dict)

    @classmethod
    def from_iterable(cls, xs: Iterable[X]) -> "Heap[X]":
        _heap = cls()
        for x in xs:
            _heap.insert(x)
        return _heap

    @classmethod
    def from_raw(cls, xs: list[X]) -> "Heap[X]":
        _arr = xs[:]
        return cls(_arr=_arr, _pos={v: k for k, v in enumerate(_arr)})

    def __bool__(self) -> bool:
        return bool(self._arr)

    def __len__(self) -> int:
        return len(self._arr)

    @staticmethod
    def parent(i: int) -> int:
        _res = i // 2
        return _res if i % 2 else _res - 1

    @staticmethod
    def children(i: int) -> Tuple[int, int]:
        _db = (i + 1) << 1
        return _db - 1, _db

    def insert(self, x: X) -> None:
        self._pos[x.name] = _next_leaf = len(self._arr)
        self._arr.append(x)

        # Keep heap invariant -> bubble-up
        self._bubble_up(_next_leaf)

    @property
    def root(self) -> Optional[X]:
        return self._arr[0] if self._arr else None

    def extract_min(self) -> X:
        self._swap(0, -1)
        root = self._poplast()
        self._bubble_down()
        return root

    def delete(self, x_name: Hashable) -> X:
        _ind, _replace = self._pos[x_name], self._arr[-1]
        self._swap(_ind, -1)
        ret = self._poplast()

        # if we deleted the root => invariably bubble down
        if _ind == 0:
            self._bubble_down()
            return ret

        if _replace.key <= self._arr[self.parent(_ind)].key:
            # replacement smaller than its parent => bubble up
            self._bubble_up(_ind)
        else:
            # replacement greater than its parent => bubble down
            self._bubble_down(_ind)

        return ret

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

    def _poplast(self) -> X:
        _ret = self._arr.pop()
        del self._pos[_ret.name]
        return _ret

    def _swap(self, i: int, j: int) -> None:
        i_el, j_el = self._arr[i], self._arr[j]
        self._pos[i_el.name] = j
        self._pos[j_el.name] = i
        self._arr[i], self._arr[j] = j_el, i_el

    def _children(self, i: int) -> List[int]:
        return [_ for _ in self.children(i) if _ < len(self._arr)]

    def as_dict(self, i: int = 0) -> Union[dict, X]:
        if not self._arr:
            return {}

        _children = self._children(i)
        _val = self._arr[i]
        if not _children:
            return _val
        return {_val: list(map(self.as_dict, _children))}
