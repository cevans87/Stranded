from __future__ import absolute_import

import typing

import pytest

from stranded.asyncio.composer import Composer
from stranded.abc import composer as abc_composer


@pytest.mark.asyncio
async def test_or_calls_each_composee() -> None:
    calls: list[tuple[str, int]] = []

    @Composer()
    async def foo(v: int) -> int:
        calls.append(('foo', v))
        return v + 1

    @Composer()
    async def bar(v: int) -> int:
        calls.append(('bar', v))
        return v * 10

    @Composer()
    async def baz(v: int) -> int:
        calls.append(('baz', v))
        return v - 3

    result = await (foo | bar | baz)(7)

    assert calls == [('foo', 7), ('bar', 8), ('baz', 80)]
    assert result == 77


@pytest.mark.asyncio
async def test_composed_or_extends_with_composed() -> None:
    @Composer()
    async def foo(v: int) -> int: return v + 1

    @Composer()
    async def bar(v: int) -> int: return v * 10

    @Composer()
    async def baz(v: int) -> int: return v - 3

    composed = (foo | bar) | baz
    assert await composed(7) == 77


@pytest.mark.asyncio
async def test_composed_or_extends_with_composed() -> None:
    @Composer()
    async def foo(v: int) -> int: return v + 1

    @Composer()
    async def bar(v: int) -> int: return v * 10

    @Composer()
    async def baz(v: int) -> int: return v - 3

    @Composer()
    async def qux(v: int) -> int: return v + 100

    composed = (foo | bar) | (baz | qux)
    assert await composed(7) == 177


@pytest.mark.asyncio
async def test_composee_exception_propagates() -> None:
    @Composer()
    async def boom() -> None:
        raise ValueError('boom')

    with pytest.raises(ValueError, match='boom'):
        await boom()


@pytest.mark.asyncio
async def test_raise_skips_downstream_composee() -> None:
    inner_called = False

    @Composer()
    async def boom(v: int) -> int:
        raise ValueError('boom')

    @Composer()
    async def inner(v: int) -> int:
        nonlocal inner_called
        inner_called = True
        return v

    with pytest.raises(ValueError, match='boom'):
        await (boom | inner)(0)

    assert inner_called is False


@pytest.mark.asyncio
async def test_raise_dataclass_carries_exception() -> None:
    raise_ = abc_composer.Raise(
        exc_type=ValueError,
        exc_val=ValueError('x'),
        exc_tb=None,
    )
    assert raise_.exc_type is ValueError
    assert isinstance(raise_.exc_val, ValueError)


@pytest.mark.asyncio
async def test_composee_stop_propagates() -> None:
    @Composer()
    async def cancelled() -> None:
        raise abc_composer.Stop()

    with pytest.raises(abc_composer.Stop):
        await cancelled()


@pytest.mark.asyncio
async def test_stop_skips_downstream_composee() -> None:
    inner_called = False

    @Composer()
    async def cancelled(v: int) -> int:
        raise abc_composer.Stop()

    @Composer()
    async def inner(v: int) -> int:
        nonlocal inner_called
        inner_called = True
        return v

    with pytest.raises(abc_composer.Stop):
        await (cancelled | inner)(0)

    assert inner_called is False


@pytest.mark.asyncio
async def test_stop_is_not_caught_by_except_exception() -> None:
    swallowed = False

    @Composer()
    async def cancelled() -> None:
        nonlocal swallowed
        try:
            raise abc_composer.Stop()
        except Exception:  # noqa
            swallowed = True

    with pytest.raises(abc_composer.Stop):
        await cancelled()

    assert swallowed is False


@pytest.mark.asyncio
async def test_method() -> None:

    class Foo:

        @Composer()
        async def bar(self, v: int) -> dict[str, object]:
            return locals()

    assert await (foo := Foo()).bar(42) == {'self': foo, 'v': 42}


@pytest.mark.asyncio
async def test_classmethod() -> None:

    class Foo:

        @classmethod
        @Composer()
        async def bar(cls, v: int) -> dict[str, object]:
            return locals()

    assert await Foo().bar(42) == {'cls': Foo, 'v': 42}


@pytest.mark.asyncio
async def test_staticmethod() -> None:

    class Foo:
        v: typing.ClassVar[int]

        @staticmethod
        @Composer()
        async def bar(v: int) -> dict[str, object]:
            return locals()

    assert await Foo.bar(42) == {'v': 42}


if __name__ == '__main__':
    pytest.main()
