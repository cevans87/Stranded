from __future__ import absolute_import

import threading
import typing

import pytest

from stranded import Composer, Decorator, Scheduler


def test_scheduler_inside_composer() -> None:
    @Decorator()
    def foo(x: int) -> int:
        return x + 1

    @Scheduler(max_workers=2)
    def bar(x: int) -> int:
        return x * 10

    composed: typing.Any = Composer()(foo, bar)  # type: ignore[arg-type]
    assert composed.call_sync(7) == 80


def test_scheduler_wraps_composed_with_metadata_preserved() -> None:
    @Decorator()
    def foo(x: int) -> int:
        """foo doc"""
        return x + 1

    @Decorator()
    def bar(x: int) -> int:
        """bar doc"""
        return x * 10

    composed: typing.Any = Composer()(foo, bar)  # type: ignore[arg-type]
    wrapped = Scheduler(max_workers=2)(composed)

    assert wrapped.__name__ == composed.__name__
    assert wrapped.__doc__ == composed.__doc__


def test_scheduler_wrapping_composed_runs_each_member_on_backend() -> None:
    caller = threading.get_ident()
    tids: list[int] = []

    @Decorator()
    def foo() -> int:
        tids.append(threading.get_ident())
        return 0

    @Decorator()
    def bar(_: int) -> int:
        tids.append(threading.get_ident())
        return 0

    composed: typing.Any = Composer()(foo, bar)  # type: ignore[arg-type]
    Scheduler(max_workers=2)(composed).call_sync()

    # Each member ran on a worker thread (not the caller thread).
    assert all(t != caller for t in tids), tids


if __name__ == '__main__':
    pytest.main()
