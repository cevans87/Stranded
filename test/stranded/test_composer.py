from __future__ import absolute_import

import typing

import pytest

from stranded import Composer


def test_base() -> None:
    @Composer()
    def foo() -> None:
        ...

    foo()


@pytest.mark.asyncio
async def test_async_method() -> None:

    class Foo:

        @Composer()
        async def bar(self, v: int) -> dict[str, object]:
            return locals()

    assert await (foo := Foo()).bar(42) == {'self': foo, 'v': 42}


def test_multi_method() -> None:

    class Foo:

        @Composer()
        def bar(self, v: int) -> dict[str, object]:
            return locals()

    assert (foo := Foo()).bar(42) == {'self': foo, 'v': 42}


@pytest.mark.asyncio
async def test_async_classmethod() -> None:

    class Foo:

        @classmethod
        @Composer()
        async def bar(cls, v: int) -> dict[str, object]:
            return locals()

    assert await Foo().bar(42) == {'cls': Foo, 'v': 42}


def test_multi_classmethod() -> None:

    class Foo:

        @classmethod
        @Composer()
        def bar(cls, v: int) -> dict[str, object]:
            return locals()

    assert Foo().bar(42) == {'cls': Foo, 'v': 42}


@pytest.mark.asyncio
async def test_async_staticmethod() -> None:

    class Foo:
        v: typing.ClassVar[int]

        @staticmethod
        @Composer()
        async def bar(v: int) -> dict[str, object]:
            return locals()

    assert await Foo.bar(42) == {'v': 42}


def test_multi_staticmethod() -> None:

    class Foo:

        @staticmethod
        @Composer()
        def bar(v: int) -> dict[str, object]:
            return locals()

    assert Foo.bar(42) == {'v': 42}


if __name__ == '__main__':
    pytest.main()
