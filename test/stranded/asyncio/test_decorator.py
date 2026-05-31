from __future__ import absolute_import

import pytest

from stranded import Decorator
from stranded.abc import decorator as abc_decorator


@pytest.mark.asyncio
async def test_or_calls_each_decoratee() -> None:
    calls: list[tuple[str, int]] = []

    @Decorator()
    async def foo(v: int) -> int:
        calls.append(('foo', v))
        return v + 1

    @Decorator()
    async def bar(v: int) -> int:
        calls.append(('bar', v))
        return v * 10

    @Decorator()
    async def baz(v: int) -> int:
        calls.append(('baz', v))
        return v - 3

    result = await (foo | bar | baz)(7)

    assert calls == [('foo', 7), ('bar', 8), ('baz', 80)]
    assert result == 77


@pytest.mark.asyncio
async def test_composed_or_extends_with_decorated() -> None:
    @Decorator()
    async def foo(v: int) -> int: return v + 1

    @Decorator()
    async def bar(v: int) -> int: return v * 10

    @Decorator()
    async def baz(v: int) -> int: return v - 3

    composed = (foo | bar) | baz
    assert await composed(7) == 77


@pytest.mark.asyncio
async def test_composed_or_extends_with_composed() -> None:
    @Decorator()
    async def foo(v: int) -> int: return v + 1

    @Decorator()
    async def bar(v: int) -> int: return v * 10

    @Decorator()
    async def baz(v: int) -> int: return v - 3

    @Decorator()
    async def qux(v: int) -> int: return v + 100

    composed = (foo | bar) | (baz | qux)
    assert await composed(7) == 177


@pytest.mark.asyncio
async def test_decoratee_exception_propagates() -> None:
    @Decorator()
    async def boom() -> None:
        raise ValueError('boom')

    with pytest.raises(ValueError, match='boom'):
        await boom()


@pytest.mark.asyncio
async def test_raise_skips_downstream_decoratee() -> None:
    inner_called = False

    @Decorator()
    async def boom(v: int) -> int:
        raise ValueError('boom')

    @Decorator()
    async def inner(v: int) -> int:
        nonlocal inner_called
        inner_called = True
        return v

    with pytest.raises(ValueError, match='boom'):
        await (boom | inner)(0)

    assert inner_called is False


@pytest.mark.asyncio
async def test_raise_dataclass_carries_exception() -> None:
    raise_ = abc_decorator.Raise(
        exc_type=ValueError,
        exc_val=ValueError('x'),
        exc_tb=None,
    )
    assert raise_.exc_type is ValueError
    assert isinstance(raise_.exc_val, ValueError)


@pytest.mark.asyncio
async def test_decoratee_stop_propagates() -> None:
    @Decorator()
    async def cancelled() -> None:
        raise abc_decorator.Stop()

    with pytest.raises(abc_decorator.Stop):
        await cancelled()


@pytest.mark.asyncio
async def test_stop_skips_downstream_decoratee() -> None:
    inner_called = False

    @Decorator()
    async def cancelled(v: int) -> int:
        raise abc_decorator.Stop()

    @Decorator()
    async def inner(v: int) -> int:
        nonlocal inner_called
        inner_called = True
        return v

    with pytest.raises(abc_decorator.Stop):
        await (cancelled | inner)(0)

    assert inner_called is False


@pytest.mark.asyncio
async def test_stop_is_not_caught_by_except_exception() -> None:
    swallowed = False

    @Decorator()
    async def cancelled() -> None:
        nonlocal swallowed
        try:
            raise abc_decorator.Stop()
        except Exception:  # noqa
            swallowed = True

    with pytest.raises(abc_decorator.Stop):
        await cancelled()

    assert swallowed is False


if __name__ == '__main__':
    pytest.main()
