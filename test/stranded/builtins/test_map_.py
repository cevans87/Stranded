import asyncio
import typing

import pytest

from stranded.builtins import Map


@pytest.fixture(scope='module')
def set_event_loop() -> typing.Generator[None]:
    """All async tests execute eagerly.

    Upon task creation return, we can be sure that the task has gotten to a point that it is either blocked or done.
    """

    eager_loop = asyncio.new_event_loop()
    eager_loop.set_task_factory(asyncio.eager_task_factory)
    asyncio.set_event_loop(eager_loop)
    yield
    asyncio.set_event_loop(None)
    eager_loop.close()


def test_threading_map_applies_sync_function() -> None:
    def inputs(vs: set[int]) -> typing.Iterable:
        for v in vs:
            yield (v,), {}

    @Map()
    def foo(i: int) -> int:
        return -i

    assert {i for i in foo(inputs({1, 2, 3, 4}))} == {-1, -2, -3, -4}


@pytest.mark.asyncio
async def test_asyncio_map_applies_async_function() -> None:
    async def inputs(vs: set[int]) -> typing.AsyncIterable:
        for v in vs:
            yield (v,), {}

    @Map()
    async def foo(i: int) -> int:
        return -i

    assert {i async for i in foo(inputs({1, 2, 3, 4}))} == {-1, -2, -3, -4}
