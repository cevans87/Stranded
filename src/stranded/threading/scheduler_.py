from __future__ import annotations

import asyncio
import atexit
import concurrent.futures
import dataclasses
import functools
import inspect
import typing

from . import composer_
from ..abc import scheduler_


Raise = composer_.Raise
Stop = composer_.Stop
Param = composer_.Param
Return = composer_.Return


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], scheduler_.Composee[ParamT, RetT], typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], scheduler_.Connect[ParamT, RetT]): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer_.Exit[ParamT, RetT], scheduler_.Exit[ParamT, RetT]): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], scheduler_.Enter[ParamT, RetT]):
    @typing.overload  # type: ignore[override]
    def __call__(self, value: Param[ParamT], /) -> tuple[composer_.Exit[ParamT, RetT], composer_.Composee[ParamT, RetT]]: ...
    @typing.overload
    def __call__(self, value: Raise | Return[RetT] | Stop, /) -> tuple[()]: ...
    def __call__(
        self, value: Param[ParamT] | Raise | Return[RetT] | Stop, /,
    ) -> tuple[composer_.Exit[ParamT, RetT], composer_.Composee[ParamT, RetT]] | tuple[()]:
        if not isinstance(value, Param):
            return ()
        scheduler: Scheduler[ParamT, RetT] = typing.cast('Scheduler[ParamT, RetT]', self.composer)
        inner = self.composee

        def wrapped(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            return scheduler.submit_sync(inner, args, kwargs)

        return self.exit_t(enter=self), typing.cast(composer_.Composee[ParamT, RetT], wrapped)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], scheduler_.Composed[ParamT, RetT]): ...


_thread_pools: dict[tuple[int | None, str], concurrent.futures.ThreadPoolExecutor] = {}


def _shared_thread_pool(
    max_workers: int | None,
    thread_name_prefix: str,
) -> concurrent.futures.ThreadPoolExecutor:
    key = (max_workers, thread_name_prefix)
    pool = _thread_pools.get(key)
    if pool is None:
        pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix=thread_name_prefix,
        )
        _thread_pools[key] = pool
    return pool


def _shutdown_all() -> None:
    for pool in _thread_pools.values():
        pool.shutdown(wait=False)
    _thread_pools.clear()


atexit.register(_shutdown_all)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheduler[**ParamT = ..., RetT = typing.Any](composer_.Composer[ParamT, RetT], scheduler_.Scheduler[ParamT, RetT]):
    composee_t: typing.ClassVar = Composee
    connect_t: typing.ClassVar = Connect
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    composed_t: typing.ClassVar = Composed

    max_workers: int | None = None
    thread_name_prefix: str = 'stranded'

    def submit_sync(
        self,
        fn: typing.Callable[..., typing.Any],
        args: tuple[typing.Any, ...],
        kwargs: dict[str, typing.Any],
    ) -> typing.Any:
        pool = _shared_thread_pool(self.max_workers, self.thread_name_prefix)
        return pool.submit(fn, *args, **kwargs).result()

    async def submit_async(
        self,
        fn: typing.Callable[..., typing.Any],
        args: tuple[typing.Any, ...],
        kwargs: dict[str, typing.Any],
    ) -> typing.Any:
        loop = asyncio.get_running_loop()
        pool = _shared_thread_pool(self.max_workers, self.thread_name_prefix)
        if inspect.iscoroutinefunction(fn):
            def runner() -> typing.Any:
                return asyncio.run(fn(*args, **kwargs))
            return await loop.run_in_executor(pool, runner)
        return await loop.run_in_executor(pool, functools.partial(fn, *args, **kwargs))
