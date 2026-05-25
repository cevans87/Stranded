from __future__ import absolute_import

import typing

import pytest

from stranded import Decorator
from stranded.composer import Composer


def test_call_sync_with_async_decoratee_uses_asyncio_run() -> None:
    @Decorator()
    async def foo(v: int) -> int: return v + 1

    @Decorator()
    async def bar(v: int) -> int: return v * 10

    composed: typing.Any = Composer()(foo, bar)  # type: ignore[arg-type]
    assert composed.call_sync(7) == 80


@pytest.mark.asyncio
async def test_call_async_with_sync_decoratee_runs_inline() -> None:
    @Decorator()
    def foo(v: int) -> int: return v + 1

    @Decorator()
    def bar(v: int) -> int: return v * 10

    composed: typing.Any = Composer()(foo, bar)  # type: ignore[arg-type]
    assert await composed.call_async(7) == 80


@pytest.mark.asyncio
async def test_call_async_mixed_sync_and_async_decorateds() -> None:
    @Decorator()
    def foo(v: int) -> int: return v + 1

    @Decorator()
    async def bar(v: int) -> int: return v * 10

    @Decorator()
    def baz(v: int) -> int: return v - 3

    composed: typing.Any = Composer()(foo, bar, baz)  # type: ignore[arg-type]
    assert await composed.call_async(7) == 77


def test_call_sync_mixed_sync_and_async_decorateds() -> None:
    @Decorator()
    def foo(v: int) -> int: return v + 1

    @Decorator()
    async def bar(v: int) -> int: return v * 10

    @Decorator()
    def baz(v: int) -> int: return v - 3

    composed: typing.Any = Composer()(foo, bar, baz)  # type: ignore[arg-type]
    assert composed.call_sync(7) == 77


if __name__ == '__main__':
    pytest.main()
