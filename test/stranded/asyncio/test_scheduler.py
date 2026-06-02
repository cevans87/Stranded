from __future__ import absolute_import

import asyncio
import threading

import pytest

from stranded.asyncio.scheduler_ import Scheduler


@pytest.mark.asyncio
async def test_scheduler_wraps_coroutine_as_task() -> None:
    @Scheduler()
    async def f(x: int) -> int:
        await asyncio.sleep(0)
        return x * 5

    assert await f(7) == 35


@pytest.mark.asyncio
async def test_scheduler_runs_sync_fn_inline() -> None:
    caller_tid = threading.get_ident()

    @Scheduler()
    def f() -> int:
        # When asyncio.Scheduler composes a sync fn, it runs inline (same thread).
        return threading.get_ident()

    # The asyncio scheduler turns a sync callee awaitable; the identity-typed
    # composer keeps the sync `() -> int` signature, so mypy can't see the await.
    assert await f() == caller_tid  # type: ignore[misc]


if __name__ == '__main__':
    pytest.main()
