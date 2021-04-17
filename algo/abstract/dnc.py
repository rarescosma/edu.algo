"""DnC abstraction."""
import abc
import itertools
from operator import add
from typing import Callable, Generic, List, Optional, TypeVar

from more_itertools import grouper

A = TypeVar("A")
_T = TypeVar("_T", bound="SupportsMerge")


class SupportsMerge(Generic[A], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __add__(self, other: Optional[A] = None) -> A:
        pass


def divide_and_conquer(
    ys: List[_T],
    starmap: Callable = itertools.starmap,
) -> List[_T]:
    while len(ys) > 1:
        ys = list(starmap(add, grouper(ys, 2)))
    return ys
