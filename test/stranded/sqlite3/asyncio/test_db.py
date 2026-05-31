import pathlib
import tempfile
import typing

import pytest

from stranded.sqlite3.asyncio import Db


@pytest.fixture
def path() -> typing.Generator[pathlib.Path, None, None]:
    with tempfile.NamedTemporaryFile() as f:
        yield pathlib.Path(f.name)


@pytest.mark.asyncio
async def test_zero_args(path: pathlib.Path) -> None:
    call_count = 0

    @Db(path=path)
    async def foo() -> None:
        nonlocal call_count
        call_count += 1

    await foo()
    await foo()
    assert call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize('arg', [None, 1, 'foo', 0.0])
async def test_primitive_arg(path: pathlib.Path, arg: object) -> None:
    call_count = 0

    @Db(path=path)
    async def foo(_: object) -> None:
        nonlocal call_count
        call_count += 1

    await foo(arg)
    await foo(arg)
    assert call_count == 1


@pytest.mark.asyncio
async def test_method(path: pathlib.Path) -> None:
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


@pytest.mark.asyncio
async def test_classmethod(path: pathlib.Path) -> None:
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


@pytest.mark.asyncio
async def test_staticmethod(path: pathlib.Path) -> None:
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
