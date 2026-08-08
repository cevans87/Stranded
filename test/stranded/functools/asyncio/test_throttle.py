import asyncio
import gc
import weakref

import pytest

from stranded.functools.asyncio import Throttle


@pytest.mark.asyncio
async def test_throttle_additive_increase_adds_1() -> None:
    event = asyncio.Event()
    n_running = 0

    @Throttle()
    async def foo() -> None:
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


@pytest.mark.asyncio
async def test_method_does_not_keep_its_instance_alive() -> None:

    class Foo:
        @Throttle()
        async def foo(self) -> None: ...

    foo = Foo()
    await foo.foo()  # type: ignore[call-arg]
    foo_ref = weakref.ref(foo)

    del foo
    gc.collect()
    assert foo_ref() is None
