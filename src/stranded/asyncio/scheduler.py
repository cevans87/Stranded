from __future__ import annotations

import asyncio
import dataclasses
import inspect
import typing

from . import composer
from ..abc import scheduler as scheduler_


Raise = composer.Raise
Stop = composer.Stop
Param = composer.Param
Return = composer.Return


@typing.runtime_checkable
class Composee[**ParamT, RetT](
    composer.Composee[ParamT, RetT],
    scheduler_.Composee[ParamT, RetT],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](
    composer.Connect[ParamT, RetT],
    scheduler_.Connect[ParamT, RetT],
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    composer.Exit[ParamT, RetT],
    scheduler_.Exit[ParamT, RetT],
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    composer.Enter[ParamT, RetT],
    scheduler_.Enter[ParamT, RetT],
):
    @typing.overload  # type: ignore[override]
    async def __call__(self, value: Param[ParamT], /) -> tuple[composer.Exit[ParamT, RetT], composer.Composee[ParamT, RetT]]: ...
    @typing.overload
    async def __call__(self, value: Raise | Return[RetT] | Stop, /) -> tuple[()]: ...
    async def __call__(
        self, value: Param[ParamT] | Raise | Return[RetT] | Stop, /,
    ) -> tuple[composer.Exit[ParamT, RetT], composer.Composee[ParamT, RetT]] | tuple[()]:
        if not isinstance(value, Param):
            return ()
        scheduler: Scheduler[ParamT, RetT] = typing.cast('Scheduler[ParamT, RetT]', self.composer)
        inner = self.composee

        async def wrapped(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            return await scheduler.submit_async(inner, args, kwargs)

        return self.exit_t(enter=self), typing.cast(composer.Composee[ParamT, RetT], wrapped)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](
    composer.Composed[ParamT, RetT],
    scheduler_.Composed[ParamT, RetT],
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheduler[**ParamT = ..., RetT = typing.Any](
    composer.Composer[ParamT, RetT],
    scheduler_.Scheduler[ParamT, RetT],
):
    composee_t: typing.ClassVar = Composee
    connect_t: typing.ClassVar = Connect
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    composed_t: typing.ClassVar = Composed

    loop: asyncio.AbstractEventLoop | None = None

    def submit_sync(
        self,
        fn: typing.Callable[..., typing.Any],
        args: tuple[typing.Any, ...],
        kwargs: dict[str, typing.Any],
    ) -> typing.Any:
        if inspect.iscoroutinefunction(fn):
            return asyncio.run(fn(*args, **kwargs))
        return fn(*args, **kwargs)

    async def submit_async(
        self,
        fn: typing.Callable[..., typing.Any],
        args: tuple[typing.Any, ...],
        kwargs: dict[str, typing.Any],
    ) -> typing.Any:
        if inspect.iscoroutinefunction(fn):
            coro = fn(*args, **kwargs)
            if self.loop is None or self.loop is asyncio.get_running_loop():
                return await asyncio.ensure_future(coro)
            future = asyncio.run_coroutine_threadsafe(coro, self.loop)
            return await asyncio.wrap_future(future)
        return fn(*args, **kwargs)
