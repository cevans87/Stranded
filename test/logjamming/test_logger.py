import asyncio
import logging
import sys

import pytest

from logjamming import Logger


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


@pytest.fixture(autouse=True)
def event_loop() -> asyncio.AbstractEventLoop:
    """All async tests execute eagerly.

    Upon task creation return, we can be sure that the task has gotten to a point that it is either blocked or done.
    """

    eager_loop = asyncio.new_event_loop()
    eager_loop.set_task_factory(asyncio.eager_task_factory)
    yield eager_loop
    eager_loop.close()


@pytest.mark.asyncio
async def test_zero_args() -> None:

    @Logger(logger=logger)
    async def foo(bar: int) -> int:
        return 42

    await foo(777)
