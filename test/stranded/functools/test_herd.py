import asyncio
import typing

import pytest
import pytest_asyncio

from stranded.functools import Herd


@pytest_asyncio.fixture(autouse=True)
async def set_eager_task_factory() -> typing.AsyncGenerator[None, None]:
    """All async tests execute eagerly.

    Upon task creation return, we can be sure that the task has gotten to a point that it is either blocked or done.
    """

    asyncio.get_running_loop().set_task_factory(asyncio.eager_task_factory)
    yield


@pytest.mark.asyncio
async def test_does_not_memoize() -> None:
    call_count = 0

    @Herd()
    async def foo() -> None:
        nonlocal call_count
        call_count += 1

    await foo()
    await foo()
    assert call_count == 2


@pytest.mark.asyncio
async def test_herds_only_call_once() -> None:
    call_count = 0
    event = asyncio.Event()

    @Herd()
    async def foo() -> None:
        nonlocal call_count
        await event.wait()
        call_count += 1

    futures = [asyncio.get_event_loop().create_task(foo()) for _ in range(10)]
    event.set()
    await asyncio.gather(*futures)

    assert call_count == 1


@pytest.mark.asyncio
async def test_separate_calls_do_not_coalesce_after_completion() -> None:
    call_count = 0
    event = asyncio.Event()

    @Herd()
    async def foo() -> None:
        nonlocal call_count
        await event.wait()
        call_count += 1

    futures = [asyncio.get_event_loop().create_task(foo()) for _ in range(5)]
    event.set()
    await asyncio.gather(*futures)
    assert call_count == 1

    event.clear()
    futures = [asyncio.get_event_loop().create_task(foo()) for _ in range(5)]
    event.set()
    await asyncio.gather(*futures)
    assert call_count == 2


@pytest.mark.asyncio
async def test_different_keys_do_not_coalesce() -> None:
    call_count = 0
    event = asyncio.Event()

    @Herd()
    async def foo(_) -> None:
        nonlocal call_count
        await event.wait()
        call_count += 1

    futures = [
        asyncio.get_event_loop().create_task(foo(i % 2))
        for i in range(10)
    ]
    event.set()
    await asyncio.gather(*futures)

    assert call_count == 2


@pytest.mark.asyncio
async def test_return_value_is_shared_with_herd() -> None:
    call_count = 0
    event = asyncio.Event()

    @Herd()
    async def foo() -> int:
        nonlocal call_count
        await event.wait()
        call_count += 1
        return call_count

    futures = [asyncio.get_event_loop().create_task(foo()) for _ in range(5)]
    event.set()
    results = await asyncio.gather(*futures)

    assert call_count == 1
    assert results == [1, 1, 1, 1, 1]


@pytest.mark.asyncio
async def test_method() -> None:
    call_count = 0
    event = asyncio.Event()

    class Foo:
        @Herd()
        async def foo(self) -> int:
            nonlocal call_count
            await event.wait()
            call_count += 1
            return call_count

    foo0, foo1 = Foo(), Foo()
    futures = [
        asyncio.get_event_loop().create_task(foo0.foo()),
        asyncio.get_event_loop().create_task(foo0.foo()),
        asyncio.get_event_loop().create_task(foo1.foo()),
        asyncio.get_event_loop().create_task(foo1.foo()),
    ]
    event.set()
    await asyncio.gather(*futures)

    assert call_count == 2


@pytest.mark.asyncio
async def test_exceptions_propagate_to_herd() -> None:
    call_count = 0
    event = asyncio.Event()

    class FooException(Exception): ...

    @Herd()
    async def foo() -> None:
        nonlocal call_count
        await event.wait()
        call_count += 1
        raise FooException()

    futures = [asyncio.get_event_loop().create_task(foo()) for _ in range(5)]
    event.set()
    results = await asyncio.gather(*futures, return_exceptions=True)

    assert call_count == 1
    assert all(isinstance(r, FooException) for r in results)


@pytest.mark.asyncio
async def test_exceptions_are_not_memoized() -> None:
    call_count = 0

    class FooException(Exception): ...

    @Herd()
    async def foo() -> None:
        nonlocal call_count
        call_count += 1
        raise FooException()

    with pytest.raises(FooException):
        await foo()
    assert call_count == 1

    with pytest.raises(FooException):
        await foo()
    assert call_count == 2
