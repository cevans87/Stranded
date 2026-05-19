from __future__ import absolute_import

import pytest

from stranded import Decorator


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


if __name__ == '__main__':
    pytest.main()
