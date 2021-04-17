"""Tests for longest_seq."""
from .longest_seq import longest_seq


def test_longest_seq() -> None:
    assert longest_seq("a") == (1, "a")
    assert longest_seq("") == (0, "")
    assert longest_seq("aabaa") == (2, "ab")
    assert longest_seq("abcd") == (4, "abcd")
    assert longest_seq("abcdabcd") == (4, "abcd")
    assert longest_seq("abacfcxzxcfca") == (4, "bacf")
    assert longest_seq("abcdefgahijklmnopqrstuvwxyz") == (
        26,
        "bcdefgahijklmnopqrstuvwxyz",
    )
