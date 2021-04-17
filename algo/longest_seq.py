"""Find the longest sequence of unique characters in an ASCII string."""
import string
from typing import Tuple


def longest_seq(x: str) -> Tuple[int, str]:
    """Gist:

    scan via a sliding window whose END advances on every iteration
    but whose START only advances when we encounter a character we've
    already seen.
    """

    last_index = {_: -1 for _ in string.printable}

    win_start, win_end, max_run, max_run_slice = 0, 0, 0, (0, 0)

    print(f"\n[]{x} -> 0")

    for i, char in enumerate(x):
        win_end = i + 1
        win_start = max(win_start, last_index[char] + 1)

        run = win_end - win_start
        print(f"{x[:win_start]}[{x[win_start:win_end]}]{x[win_end:]} -> {run}")

        if run > max_run:
            max_run = run
            max_run_slice = (win_start, win_end)

        last_index[char] = i

    return max_run, x[slice(*max_run_slice)]
