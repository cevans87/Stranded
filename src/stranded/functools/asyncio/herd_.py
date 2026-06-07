import asyncio
import dataclasses
import typing

from ..abc import herd_
from ...asyncio import composer_


Raise = composer_.Raise
Stop = composer_.Stop
Param = composer_.Param
Return = composer_.Return


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], herd_.Composee[ParamT, RetT], typing.Protocol): ...


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
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], herd_.Connect[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer_.Exit[ParamT, RetT], herd_.Exit[ParamT, RetT, Future[RetT]]):
    future: Future[RetT] = dataclasses.field(default_factory=Future)

    @typing.override
    async def __call__(self, value: composer_.ValueT[ParamT, RetT], /) -> composer_.StackT:  # type: ignore[override]
        self.enter.future_by_key.pop(self.key, None)  # type: ignore[attr-defined]
        match value:
            case Param(): pass
            case Return() | Raise() | Stop(): self.future.set_value(value)

        return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], herd_.Enter[ParamT, RetT, Future[RetT]]):
    @typing.override
    async def __call__(  # type: ignore[override]
        self, value: composer_.ValueT[ParamT, RetT], /,
    ) -> composer_.StackT:
        match value:
            case Param(): return self._dispatch(*value.args, **value.kwargs)  # type: ignore[return-value]
            case _: return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], herd_.Composed[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Herd[**ParamT = ..., RetT = typing.Any](composer_.Composer[ParamT, RetT], herd_.Herd[ParamT, RetT]):
    Composee: typing.ClassVar = Composee
    Connect: typing.ClassVar = Connect
    Exit: typing.ClassVar = Exit  # type: ignore[assignment]
    Enter: typing.ClassVar = Enter
    Composed: typing.ClassVar = Composed

    @property
    @typing.override
    def future_t(self) -> type[Future[RetT]]:
        return Future


Composer = Herd
herd = Herd()
