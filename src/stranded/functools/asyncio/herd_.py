import asyncio
import dataclasses
import typing

from ..abc import herd_
from ...asyncio import decorator


Raise = decorator.Raise
Stop = decorator.Stop
Param = decorator.Param
Return = decorator.Return


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    herd_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Future[RetT](herd_.Future[RetT]):
    future: asyncio.Future[RetT] = dataclasses.field(default_factory=asyncio.Future)

    @typing.override
    def set_value(self, value: Return[RetT] | Raise | Stop) -> None:
        match value:
            case Return(ret=ret): self.future.set_result(ret)
            case Raise() as raise_: self.future.set_exception(raise_.exc_val)
            case Stop() as stop_: self.future.set_exception(stop_)

    @typing.override
    async def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> RetT:
        return await self.future


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT](
    decorator.Send[ParamT, RetT],
    herd_.Send[ParamT, RetT, Future[RetT]],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](
    decorator.Receive[ParamT, RetT],
    herd_.Receive[ParamT, RetT, Future[RetT]],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    herd_.Exit[ParamT, RetT, Future[RetT]],
):
    future: Future[RetT] = dataclasses.field(default_factory=Future)

    @typing.override
    async def __call__(self, value: Param[ParamT] | Raise | Return[RetT] | Stop) -> tuple[()]:  # type: ignore[override]
        self.enter.decorated.future_by_key.pop(self.key, None)  # type: ignore[attr-defined]
        match value:
            case Param(): pass
            case Return() | Raise() | Stop(): self.future.set_value(value)

        return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    herd_.Enter[ParamT, RetT],
):
    @typing.override
    async def __call__(  # type: ignore[override]
        self, value: Param[ParamT] | Raise | Return[RetT] | Stop,
    ) -> tuple[Exit[ParamT, RetT], Decoratee[ParamT, RetT]] | tuple[Future[RetT]] | tuple[()]:
        match value:
            case Param(): return self._dispatch(*value.args, **value.kwargs)  # type: ignore[return-value]
            case _: return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    herd_.Decorated[ParamT, RetT, Future[RetT]],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Herd[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    herd_.Herd[ParamT, RetT],
):
    decoratee_t: typing.ClassVar = Decoratee
    receive_t: typing.ClassVar = Receive
    send_t: typing.ClassVar = Send
    exit_t: typing.ClassVar = Exit  # type: ignore[assignment]
    enter_t: typing.ClassVar = Enter
    decorated_t: typing.ClassVar = Decorated

    @property
    @typing.override
    def future_t(self) -> type[Future[RetT]]:
        return Future


Decorator = Herd
herd: Herd[..., typing.Any] = Herd()
