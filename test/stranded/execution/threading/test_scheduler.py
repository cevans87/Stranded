from __future__ import absolute_import

import asyncio
import threading

import pytest

from stranded.threading.composer_ import Composer
from stranded.execution.threading.scheduler_ import Scheduler


def _raise() -> None:
    raise ValueError('boom')


def test_scheduler_runs_composed_pipeline_on_its_context() -> None:
    # Mirrors the canonical std::execution (C++26) example:
    #
    #   scheduler auto sch    = thread_pool.get_scheduler();
    #   sender auto begin     = schedule(sch);
    #   sender auto hi        = then(begin, []{ return 13; });
    #   sender auto add_42    = then(hi, [](int v){ return v + 42; });
    #   auto [i] = this_thread::sync_wait(add_42).value();   // i == 55
    #
    # Stranded analog: each Composer-wrapped callee is a "sender", `|` chains
    # them (like `then`) into one Composed pipeline, the Scheduler transfers the
    # whole pipeline onto its execution context (`on(sch, work)`), and the
    # synchronous call blocks for the result (`sync_wait`). The Scheduler's Enter
    # submits the nested pipeline to the pool, so every stage runs off the
    # caller's thread.
    caller = threading.get_ident()
    ran_on: list[int] = []

    @Composer()
    def thirteen(_seed: int) -> int:
        ran_on.append(threading.get_ident())
        return 13

    @Composer()
    def add_42(v: int) -> int:
        ran_on.append(threading.get_ident())
        return v + 42

    work = Scheduler(max_workers=2)(thirteen | add_42)

    assert work(0) == 55
    assert ran_on and all(tid != caller for tid in ran_on)


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
