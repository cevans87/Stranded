from __future__ import absolute_import

import pytest

from stranded import Decorator
from stranded.abc import decorator as abc_decorator


@pytest.mark.asyncio
async def test_or_combines_metadata() -> None:
    @Decorator()
    async def foo(v):
        """foo doc"""
        return v + 1

    @Decorator()
    async def bar(v):
        """bar doc"""
        return v * 2

    combined = foo | bar

    assert combined.__doc__ == f'{foo.__doc__}\n\n{bar.__doc__}'
    assert combined.__name__ == f'{foo.__name__}, {bar.__name__}'
    assert combined.__qualname__ == f'{foo.__qualname__}, {bar.__qualname__}'
    assert combined.__module__ == f'{foo.__module__}, {bar.__module__}'


@pytest.mark.asyncio
async def test_or_calls_each_decoratee() -> None:
    calls: list[tuple[str, int]] = []

    @Decorator()
    async def foo(v):
        calls.append(('foo', v))
        return v + 1

    @Decorator()
    async def bar(v):
        calls.append(('bar', v))
        return v * 10

    @Decorator()
    async def baz(v):
        calls.append(('baz', v))
        return v - 3

    result = await (foo | bar | baz)(7)

    assert calls == [('foo', 7), ('bar', 8), ('baz', 80)]
    assert result == 77


@pytest.mark.asyncio
async def test_or_stack_grows() -> None:
    @Decorator()
    async def foo(v):
        return v

    @Decorator()
    async def bar(v):
        return v

    @Decorator()
    async def baz(v):
        return v

    assert foo.stack == ()
    assert (foo | bar).stack != ()
    assert len((foo | bar | baz).stack) > len((foo | bar).stack)


@pytest.mark.asyncio
async def test_decoratee_exception_propagates() -> None:
    @Decorator()
    async def boom():
        raise ValueError('boom')

    with pytest.raises(ValueError, match='boom'):
        await boom()


@pytest.mark.asyncio
async def test_raise_skips_downstream_decoratee() -> None:
    inner_called = False

    @Decorator()
    async def boom():
        raise ValueError('boom')

    @Decorator()
    async def inner(v):
        nonlocal inner_called
        inner_called = True
        return v

    with pytest.raises(ValueError, match='boom'):
        await (boom | inner)()

    assert inner_called is False


@pytest.mark.asyncio
async def test_raise_dataclass_carries_exception() -> None:
    raise_ = abc_decorator.Raise(
        exc_type=ValueError,
        exc_val=ValueError('x'),
        exc_tb=None,  # type: ignore[arg-type]
    )
    assert raise_.exc_type is ValueError
    assert isinstance(raise_.exc_val, ValueError)


@pytest.mark.asyncio
async def test_decoratee_stop_propagates() -> None:
    @Decorator()
    async def cancelled():
        raise abc_decorator.Stop()

    with pytest.raises(abc_decorator.Stop):
        await cancelled()


@pytest.mark.asyncio
async def test_stop_skips_downstream_decoratee() -> None:
    inner_called = False

    @Decorator()
    async def cancelled():
        raise abc_decorator.Stop()

    @Decorator()
    async def inner(v):
        nonlocal inner_called
        inner_called = True
        return v

    with pytest.raises(abc_decorator.Stop):
        await (cancelled | inner)()

    assert inner_called is False


@pytest.mark.asyncio
async def test_stop_is_not_caught_by_except_exception() -> None:
    swallowed = False

    @Decorator()
    async def cancelled():
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
