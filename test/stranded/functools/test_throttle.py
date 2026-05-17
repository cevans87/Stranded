import asyncio
import typing

import pytest

from stranded.functools import Throttle


@pytest.fixture(scope='module')
def set_event_loop() -> typing.Generator[None, None, None]:
    """All async tests execute eagerly.

    Upon task creation return, we can be sure that the task has gotten to a point that it is either blocked or done.
    """

    eager_loop = asyncio.new_event_loop()
    eager_loop.set_task_factory(asyncio.eager_task_factory)
    asyncio.set_event_loop(eager_loop)
    yield
    asyncio.set_event_loop(None)
    eager_loop.close()


@pytest.mark.asyncio
async def test_throttle_additive_increase_adds_1() -> None:
    event = asyncio.Event()
    n_running = 0

    @Throttle()
    async def foo():
        nonlocal n_running
        n_running += 1
        await event.wait()
        n_running -= 1

        for i in range(1, 10):
            event.clear()
            async with asyncio.TaskGroup() as tg:
                for j in range(i + 1):
                    tg.create_task(foo())
                assert n_running == i
                event.set()
