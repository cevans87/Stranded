from __future__ import annotations

import asyncio
import dataclasses
import inspect
import typing

from . import composer, decorator
from ..abc import scheduler as scheduler_


Raise = decorator.Raise
Stop = decorator.Stop
Param = decorator.Param
Return = decorator.Return


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    scheduler_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    scheduler_.Exit[ParamT, RetT],
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    scheduler_.Enter[ParamT, RetT],
):
    @typing.overload  # type: ignore[override]
    async def __call__(self, value: Param[ParamT], /) -> tuple[decorator.Exit[ParamT, RetT], decorator.Decoratee[ParamT, RetT]]: ...
    @typing.overload
    async def __call__(self, value: Raise | Return[RetT] | Stop, /) -> tuple[()]: ...
    async def __call__(
        self, value: Param[ParamT] | Raise | Return[RetT] | Stop, /,
    ) -> tuple[decorator.Exit[ParamT, RetT], decorator.Decoratee[ParamT, RetT]] | tuple[()]:
        if not isinstance(value, Param):
            return ()
        scheduler: Scheduler[ParamT, RetT] = typing.cast('Scheduler[ParamT, RetT]', self.decorator)
        inner = self.decoratee

        async def wrapped(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            return await scheduler.submit_async(inner, args, kwargs)

        return self.exit_t(enter=self), typing.cast(decorator.Decoratee[ParamT, RetT], wrapped)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    scheduler_.Decorated[ParamT, RetT],
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheduler[**ParamT = ..., RetT = typing.Any](
    decorator.Decorator[ParamT, RetT],
    scheduler_.Scheduler[ParamT, RetT],
):
    decoratee_t: typing.ClassVar = Decoratee
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    decorated_t: typing.ClassVar = Decorated
    composer_t: typing.ClassVar = composer.Composer

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
