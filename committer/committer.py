"""
Generate bogus commits for displaying messages in the stash / github
activity graph.
"""
import json
import os
import sys
from datetime import datetime, timedelta
from itertools import count
from multiprocessing.pool import Pool
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable, Optional

import sh
from cached_property import cached_property
from more_itertools import divide

from ..abstract.dnc import SupportsMerge, divide_and_conquer

ROWS = [
    "#### #  # #  # ###  ###   ##   ##",
    "#    #  # ## # #  # #  # #  # #",
    "###  #  # # ## ###  ###  #  # # ##",
    "#    #  # #  # #    # #  #  # #  #",
    "#     ##  #  # #    #  #  ##   ##",
]

_TICKS = len([_ for _ in "".join(ROWS) if _ == "#"])


YEAR = "2020"
START_DAY = datetime.strptime("2020-04-19", "%Y-%m-%d")
GIT: sh.Command = sh.git.bake(_no_out=True, _no_err=True, _no_pipe=True)
SEQ_GEN = count(0)


class Target(SupportsMerge["Target"]):
    root: Path
    dates: Iterable[datetime]
    remote: str

    git: sh.Command

    def __init__(
        self,
        root: Path,
        dates: Iterable[datetime] = (),
    ) -> None:
        self.root = root
        self.dates = dates
        self.remote = f"tmp_remote_{next(SEQ_GEN)}"
        self.git = GIT.bake(_cwd=self.cwd)
        if not (self.cwd / ".git").exists():
            self.git.init()

    @cached_property
    def cwd(self) -> Path:
        _cwd = self.root / self.remote
        _cwd.mkdir(parents=True, exist_ok=False)
        return _cwd

    def merge_into(self, cwd: Path, remove: bool = False) -> None:
        _git = GIT.bake(_cwd=cwd)
        if remove:
            _git.remote("remove", self.remote, _ok_code=[0, 2])
        _git.remote("add", "--fetch", self.remote, self.cwd.as_posix())
        _git.merge(f"{self.remote}/master", allow_unrelated_histories=True)
        if remove:
            _git.remote("remove", self.remote, _ok_code=[0, 2])

    def __add__(self, other: Optional["Target"] = None) -> "Target":
        if other is not None:
            print(f"{self.remote} ⬅💚 {other.remote}")
            other.merge_into(self.cwd)
        return self


def offset_gen() -> Iterable[bool]:
    n_cols = max(len(r) for r in ROWS)
    j_rows = [_.ljust(n_cols) for _ in ROWS]
    for col in range(n_cols):
        yield from [False, *[_[col] == "#" for _ in j_rows], False]
        #            Sun                                      Sat


def commit_dates(start_day: datetime, per_day: int) -> Iterable[datetime]:
    for idx, offset in enumerate(offset_gen()):
        if offset:
            for _ in range(15, 15 + per_day):
                yield start_day + timedelta(days=idx, minutes=_)


def spam_commits(target: Target) -> None:
    for idx, _ in enumerate(target.dates):
        _date = _.isoformat()
        target.git.commit(
            message=".",
            allow_empty=True,
            _env={
                **os.environ,
                "GIT_AUTHOR_DATE": _date,
                "GIT_COMMITTER_DATE": _date,
            },
        )
        if idx and idx % 20 == 0:
            sys.stdout.write("🐹")
            sys.stdout.flush()


def main() -> None:
    _per_day = int(sys.argv[1]) if len(sys.argv) >= 2 else 12
    _num_repos = 24
    _num_procs = min(12, _num_repos)
    _commit_dates = list(commit_dates(START_DAY, per_day=_per_day))
    _num_commits = len(_commit_dates)

    assert (_TICKS * _per_day) == _num_commits

    stats = dict(
        commits_per_day=_per_day,
        commits_per_repo=(_num_commits / _num_repos),
        num_commits=_num_commits,
        num_repos=_num_repos,
        num_procs=_num_procs,
        start_date=START_DAY.isoformat(sep=" "),
    )
    print(json.dumps(stats, indent=2))

    with TemporaryDirectory() as tmp_dir, Pool(_num_procs) as _pool:
        targets = [
            Target(Path(tmp_dir), _chunk)
            for idx, _chunk in enumerate(divide(_num_repos, _commit_dates))
        ]
        print("===> spam stage:")
        _pool.map(spam_commits, targets)
        print("\n===> merge stage:")
        for _top in divide_and_conquer(targets, _pool.starmap):
            print(f"root ⬅💚 {_top.remote}")
            _top.merge_into(Path("../fp"), remove=True)
