from __future__ import absolute_import

import asyncio
import threading

import pytest

from stranded.threading.scheduler import Scheduler


def _raise() -> None:
    raise ValueError('boom')


def test_scheduler_blocks_on_thread_pool_result() -> None:
    caller = threading.get_ident()

    @Scheduler(max_workers=2)
    def f() -> int:
        return threading.get_ident()

    assert f() != caller


def test_scheduler_propagates_exceptions() -> None:
    bang = Scheduler(max_workers=2)(_raise)
    with pytest.raises(ValueError, match='boom'):
        bang()


@pytest.mark.asyncio
async def test_scheduler_submit_async_with_coroutine_runs_in_thread_via_asyncio_run() -> None:
    caller = threading.get_ident()
    sched = Scheduler(max_workers=2)

    async def coro() -> int:
        await asyncio.sleep(0)
        return threading.get_ident()

    tid = await sched.submit_async(coro, (), {})
    assert tid != caller


if __name__ == '__main__':
    pytest.main()
