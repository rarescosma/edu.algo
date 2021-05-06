import time
from pathlib import Path
from typing import Iterable, List, NamedTuple

from algo.heap import Heap


def naive_median(numbers: List[int]) -> Iterable[int]:
    num_medians = len(numbers)
    for k in range(1, num_medians + 1):
        over = sorted(numbers[0:k])
        l_over = len(over)
        if l_over % 2:  # odd number of numbers
            yield over[(k + 1) // 2 - 1]
        else:
            yield over[k // 2 - 1]


class MinInt(NamedTuple):
    el: int

    @property
    def key(self) -> int:
        return self.el

    @property
    def name(self) -> int:
        return self.key


class MaxInt(NamedTuple):
    el: int

    @property
    def key(self) -> int:
        return -self.el

    @property
    def name(self) -> int:
        return self.key


def heap_median(numbers: List[int]) -> Iterable[int]:
    if not numbers:
        return []

    yield numbers[0]

    if len(numbers) >= 2:
        max_root, min_root = (
            (numbers[0], numbers[1])
            if numbers[0] < numbers[1]
            else (numbers[1], numbers[0])
        )
        min_heap, max_heap = Heap[MinInt](), Heap[MaxInt]()
        min_heap.insert(MinInt(min_root))
        max_heap.insert(MaxInt(max_root))
        yield max_heap.root.el

        for n in numbers[2:]:
            # insert
            if n > min_heap.root.el:
                min_heap.insert(MinInt(n))
            else:
                max_heap.insert(MaxInt(n))

            # rebalance (max_heap can be AT MOST 1 el. larger than min_heap)
            for _ in range(len(max_heap) - len(min_heap) - 1):
                min_heap.insert(MinInt(max_heap.extract_min().el))

            for _ in range(len(min_heap) - len(max_heap)):
                max_heap.insert(MaxInt(min_heap.extract_min().el))

            yield max_heap.root.el


if __name__ == "__main__":
    ints = [
        int(_.strip())
        for _ in (Path(__file__).parent / "../../data/median_maintain.txt")
        .read_text()
        .splitlines()
        if _
    ]

    t0 = time.time()
    medians = list(heap_median(ints))
    t1 = time.time()
    list(naive_median(ints))
    t2 = time.time()
    print(f"for {len(ints)} unique random integers")
    print(f"naive median maintenance took: {t2 - t1:.3f}s")
    print(f"heap-based median maintenance took: {t1 - t0:.3f}s")
    print(f"speedup is: {(t2-t1)/(t1-t0):.3f}")
    resp = sum(medians) % 10000
    print(resp)
