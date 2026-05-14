import asyncio
import pathlib
import tempfile
import typing

import pytest

from stranded.sqlite3 import Db


# TODO: Threaded tests are missing. This suite heavily relies upon determining whether coroutines are running vs
#  suspended (via asyncio.eager_task_factory). Ideally, similar functionality exists for threading. Otherwise, we need
#  to find a way to determine that thread execution has reached a certain point. Ideally without mocking synchronization
#  primitives.


@pytest.fixture(autouse=True)
def event_loop() -> typing.Generator[asyncio.AbstractEventLoop, None, None]:
    """All async tests execute eagerly.

    Upon task creation return, we can be sure that the task has gotten to a point that it is either blocked or done.
    """

    eager_loop = asyncio.new_event_loop()
    eager_loop.set_task_factory(asyncio.eager_task_factory)
    yield eager_loop
    eager_loop.close()


@pytest.fixture
def path() -> typing.Generator[pathlib.Path, None, None]:
    with tempfile.NamedTemporaryFile() as f:
        yield pathlib.Path(f.name)


@pytest.mark.asyncio
async def test_async_zero_args(path: pathlib.Path) -> None:
    call_count = 0

    @Db(path=path)
    async def foo() -> None:
        nonlocal call_count
        call_count += 1

    await foo()
    await foo()
    assert call_count == 1


def test_multi_zero_args(path: pathlib.Path) -> None:
    call_count = 0

    @Db(path=path)
    def foo() -> None:
        nonlocal call_count
        call_count += 1

    foo()
    foo()
    assert call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize('arg', [None, 1, 'foo', 0.0])
async def test_async_primitive_arg(path: pathlib.Path, arg) -> None:
    call_count = 0

    @Db(path=path)
    async def foo(_) -> None:
        nonlocal call_count
        call_count += 1

    await foo(arg)
    await foo(arg)
    assert call_count == 1


@pytest.mark.parametrize('arg', [None, 1, 'foo', 0.0])
def test_multi_primitive_arg(path: pathlib.Path, arg) -> None:
    call_count = 0

    @Db(path=path)
    def foo(_) -> None:
        nonlocal call_count
        call_count += 1

    foo(arg)
    foo(arg)
    assert call_count == 1


@pytest.mark.asyncio
async def test_async_method(path: pathlib.Path) -> None:
    call_count = 0

    class Foo:

        @Db(path=path)
        async def foo(self) -> None:
            nonlocal call_count
            call_count += 1

    foo0, foo1 = Foo(), Foo()
    await foo0.foo()
    await foo0.foo()
    assert call_count == 1

    await foo1.foo()
    await foo1.foo()
    assert call_count == 2


def test_multi_method(path: pathlib.Path) -> None:
    call_count = 0

    class Foo:

        @Db(path=path)
        def foo(self) -> None:
            nonlocal call_count
            call_count += 1

    foo0, foo1 = Foo(), Foo()
    foo0.foo()
    foo0.foo()
    assert call_count == 1

    foo1.foo()
    foo1.foo()
    assert call_count == 2


@pytest.mark.asyncio
async def test_async_classmethod(path: pathlib.Path) -> None:
    call_count = 0

    class Foo:
        @classmethod
        @Db(path=path)
        async def foo(cls) -> None:
            nonlocal call_count
            call_count += 1

    foo0, foo1 = Foo(), Foo()
    await foo0.foo()
    await foo0.foo()
    assert call_count == 1

    await foo1.foo()
    await foo1.foo()
    assert call_count == 1

    await Foo.foo()
    await Foo.foo()
    assert call_count == 1


def test_multi_classmethod(path: pathlib.Path) -> None:
    call_count = 0

    class Foo:
        @classmethod
        @Db(path=path)
        def foo(cls) -> None:
            nonlocal call_count
            call_count += 1

    foo0, foo1 = Foo(), Foo()
    foo0.foo()
    foo0.foo()
    assert call_count == 1

    foo1.foo()
    foo1.foo()
    assert call_count == 1

    Foo.foo()
    Foo.foo()
    assert call_count == 1


@pytest.mark.asyncio
async def test_async_staticmethod(path: pathlib.Path) -> None:
    call_count = 0

    class Foo:
        @staticmethod
        @Db(path=path)
        async def foo() -> None:
            nonlocal call_count
            call_count += 1

    foo0, foo1 = Foo(), Foo()
    await foo0.foo()
    await foo0.foo()
    assert call_count == 1

    await foo1.foo()
    await foo1.foo()
    assert call_count == 1

    await Foo.foo()
    await Foo.foo()
    assert call_count == 1


def test_multi_staticmethod(path: pathlib.Path) -> None:
    call_count = 0

    class Foo:
        @staticmethod
        @Db(path=path)
        def foo() -> None:
            nonlocal call_count
            call_count += 1

    foo0, foo1 = Foo(), Foo()
    foo0.foo()
    foo0.foo()
    assert call_count == 1

    foo1.foo()
    foo1.foo()
    assert call_count == 1

    Foo.foo()
    Foo.foo()
    assert call_count == 1


