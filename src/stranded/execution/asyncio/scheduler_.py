from __future__ import annotations

import asyncio
import dataclasses
import inspect
import typing

from ...asyncio import composer_
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
    async def __call__(self, value: Param[ParamT], /) -> tuple[composer_.Exit[ParamT, RetT], composer_.Composee[ParamT, RetT]]: ...
    @typing.overload
    async def __call__(self, value: Raise | Return[RetT] | Stop, /) -> tuple[()]: ...
    async def __call__(
        self, value: Param[ParamT] | Raise | Return[RetT] | Stop, /,
    ) -> tuple[composer_.Exit[ParamT, RetT], composer_.Composee[ParamT, RetT]] | tuple[()]:
        if not isinstance(value, Param):
            return ()
        scheduler: Scheduler[ParamT, RetT] = typing.cast('Scheduler[ParamT, RetT]', self.composer)
        inner = self.composee

        async def wrapped(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            return await scheduler.submit_async(inner, args, kwargs)

        return self.composer.Exit(enter=self), typing.cast(composer_.Composee[ParamT, RetT], wrapped)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], scheduler_.Composed[ParamT, RetT]): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheduler[**ParamT = ..., RetT = typing.Any](composer_.Composer[ParamT, RetT], scheduler_.Scheduler[ParamT, RetT]):
    Composee: typing.ClassVar = Composee
    Connect: typing.ClassVar = Connect
    Exit: typing.ClassVar = Exit
    Enter: typing.ClassVar = Enter
    Composed: typing.ClassVar = Composed

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
