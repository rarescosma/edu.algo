"""
Concrete use case of the DnC primitive:

MergeSort - we receive two sub-arrays from the recursive step
and perform the merge step using __add__.
"""
from dataclasses import dataclass, replace
from typing import Generic, List, Optional, TypeVar

from ..abstract.dnc import SupportsMerge

X = TypeVar("X")


@dataclass(frozen=True)
class MergeSort(SupportsMerge["MergeSort"], Generic[X]):
    values: List[X]

    @classmethod
    def pure(cls, x: X) -> "MergeSort[X]":
        return cls([x])

    def __len__(self) -> int:
        return len(self.values)

    def __add__(self, other: Optional["MergeSort"] = None) -> "MergeSort":
        if other is None:
            return self

        i, j, i_max, j_max = 0, 0, len(self), len(other)

        output: List[X] = []
        while i < i_max and j < j_max:
            if self.values[i] <= other.values[j]:
                output.append(self.values[i])
                i += 1
            else:
                output.append(other.values[j])
                j += 1

        output.extend(self.values[i:])
        output.extend(other.values[j:])
        return replace(self, values=output)
