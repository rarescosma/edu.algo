"""
Concrete use case of the DnC primitives.
"""
from dataclasses import dataclass, replace
from typing import Generic, List, Optional, TypeVar

from .dnc import SupportsMerge

C = TypeVar("C")


@dataclass(frozen=True)
class SortList(SupportsMerge["SortList"], Generic[C]):
    values: List[C]

    @classmethod
    def unit(cls, x: C) -> "SortList[C]":
        return cls([x])

    def __len__(self) -> int:
        return len(self.values)

    def __add__(self, other: Optional["SortList"] = None) -> "SortList":
        if other is None:
            return self

        i, j, i_max, j_max = 0, 0, len(self), len(other)

        output: List[C] = []
        while i < i_max and j < j_max:
            if self.values[i] < other.values[j]:
                output.append(self.values[i])
                i += 1
            else:
                output.append(other.values[j])
                j += 1

        output.extend(self.values[i:])
        output.extend(other.values[j:])
        return replace(self, values=output)
