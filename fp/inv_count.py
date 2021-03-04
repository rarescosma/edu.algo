"""
Count the number of inversions in an array by piggybacking on MergeSort
"""
from dataclasses import dataclass, replace
from typing import Generic, List, Optional, TypeVar

from .dnc import SupportsMerge

X = TypeVar("X")


@dataclass(frozen=True)
class InvCount(SupportsMerge["InvCount"], Generic[X]):
    values: List[X]
    inv_count: int = 0

    @classmethod
    def pure(cls, x: X) -> "InvCount[X]":
        return cls([x])

    def __len__(self) -> int:
        return len(self.values)

    def __add__(self, other: Optional["InvCount"] = None) -> "InvCount":
        if other is None:
            return self

        i, j, i_max, j_max = 0, 0, len(self), len(other)

        output: List[X] = []
        inv_count = 0
        while i < i_max and j < j_max:
            if self.values[i] <= other.values[j]:
                # boring case, we've copied from the left sub-array
                output.append(self.values[i])
                i += 1
            else:
                # interesting case - we've copied from right
                # accumulate remaining length of left as inversions
                output.append(other.values[j])
                inv_count += i_max - i
                j += 1

        output.extend(self.values[i:])
        output.extend(other.values[j:])
        return replace(
            self,
            values=output,
            inv_count=(self.inv_count + other.inv_count + inv_count),
        )
