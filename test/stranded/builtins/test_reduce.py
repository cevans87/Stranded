import asyncio
import typing

import pytest

from stranded.builtins import Reduce


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


def test_threading_reduce_applies_sync_function() -> None:
    def inputs(vs: set[int]) -> typing.Iterable[int]:
        for v in vs:
            yield v

    @Reduce(init=0)
    def foo(l: int, r: int) -> int:
        return l + r

    assert foo(inputs({1, 2, 3, 4})) == sum({1, 2, 3, 4})


@pytest.mark.asyncio
async def test_asyncio_reduce_applies_async_function() -> None:
    async def inputs(vs: set[int]) -> typing.AsyncIterable[int]:
        for v in vs:
            yield v

    @Reduce(init=0)
    async def foo(l: int, r: int) -> int:
        return l + r

    assert await foo(inputs({1, 2, 3, 4})) == sum({1, 2, 3, 4})


def test_threading_reduce_propagates_exception() -> None:
    def inputs(vs: set[int]) -> typing.Iterable[int]:
        for v in vs:
            yield v

    @Reduce(init=0)
    def foo(l: int, r: int) -> int:
        if r == 4:
            raise Exception()
        return l + r

    with pytest.raises(Exception):
        foo(inputs({1, 2, 3, 4}))


@pytest.mark.asyncio
async def test_asyncio_reduce_propagates_exception() -> None:
    async def inputs(vs: set[int]) -> typing.AsyncIterable[int]:
        for v in vs:
            yield v

    @Reduce(init=0)
    async def foo(l: int, r: int) -> int:
        if r == 4:
            raise Exception()
        return l + r

    with pytest.raises(Exception):
        await foo(inputs({1, 2, 3, 4}))
