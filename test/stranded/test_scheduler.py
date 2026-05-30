from __future__ import absolute_import

import asyncio
import threading
import typing

import pytest

from stranded import Composer, Decorator, Scheduler


def test_scheduler_on_sync_runs_on_worker_thread() -> None:
    caller = threading.get_ident()

    @Scheduler(max_workers=2)
    def f() -> int:
        return threading.get_ident()

    assert f() != caller


@pytest.mark.asyncio
async def test_scheduler_on_async_routes_to_asyncio_flavor() -> None:
    @Scheduler()
    async def f(x: int) -> int:
        await asyncio.sleep(0)
        return x * 4

    assert await f(7) == 28


def test_scheduler_wraps_composed_per_constituent() -> None:
    @Decorator()
    def a(x: int) -> int:
        return x + 1

    @Decorator()
    def b(x: int) -> int:
        return x * 10

    composed: typing.Any = Composer()(a, b)  # type: ignore[arg-type]
    wrapped = Scheduler(max_workers=2)(composed)

    assert wrapped.call_sync(7) == 80


def test_scheduler_nests_with_existing_decorated() -> None:
    @Decorator()
    def f(x: int) -> int:
        return x + 1

    nested = Scheduler(max_workers=2)(f)
    assert nested(7) == 8


def test_scheduler_pool_is_shared_across_instances() -> None:
    # Same key → same pool.
    from stranded.threading.scheduler import _shared_thread_pool
    p1 = _shared_thread_pool(2, 'stranded')
    p2 = _shared_thread_pool(2, 'stranded')
    assert p1 is p2


def test_top_level_scheduler_classvars_are_not_dataclass_fields() -> None:
    import dataclasses
    field_names = {f.name for f in dataclasses.fields(Scheduler)}
    assert 'composer_t' not in field_names
    assert 'decoratee_t' not in field_names
    assert 'enter_t' not in field_names
    assert 'exit_t' not in field_names
    assert 'decorated_t' not in field_names


if __name__ == '__main__':
    pytest.main()
