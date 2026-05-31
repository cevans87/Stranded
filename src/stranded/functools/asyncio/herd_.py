import asyncio
import dataclasses
import typing

from ..abc import herd_
from ...asyncio import composer


Raise = composer.Raise
Stop = composer.Stop
Param = composer.Param
Return = composer.Return


@typing.runtime_checkable
class Composee[**ParamT, RetT](
    composer.Composee[ParamT, RetT],
    herd_.Composee[ParamT, RetT],
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
class Exit[**ParamT, RetT](
    composer.Exit[ParamT, RetT],
    herd_.Exit[ParamT, RetT, Future[RetT]],
):
    future: Future[RetT] = dataclasses.field(default_factory=Future)

    @typing.override
    async def __call__(self, value: composer.ValueT[ParamT, RetT], /) -> composer.StackT:  # type: ignore[override]
        self.enter.future_by_key.pop(self.key, None)  # type: ignore[attr-defined]
        match value:
            case Param(): pass
            case Return() | Raise() | Stop(): self.future.set_value(value)

        return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    composer.Enter[ParamT, RetT],
    herd_.Enter[ParamT, RetT, Future[RetT]],
):
    @typing.override
    async def __call__(  # type: ignore[override]
        self, value: composer.ValueT[ParamT, RetT], /,
    ) -> composer.StackT:
        match value:
            case Param(): return self._dispatch(*value.args, **value.kwargs)  # type: ignore[return-value]
            case _: return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](
    composer.Composed[ParamT, RetT],
    herd_.Composed[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Herd[**ParamT, RetT](
    composer.Composer[ParamT, RetT],
    herd_.Herd[ParamT, RetT],
):
    composee_t: typing.ClassVar = Composee
    exit_t: typing.ClassVar = Exit  # type: ignore[assignment]
    enter_t: typing.ClassVar = Enter
    composed_t: typing.ClassVar = Composed

    @property
    @typing.override
    def future_t(self) -> type[Future[RetT]]:
        return Future


Composer = Herd
herd: Herd[..., typing.Any] = Herd()
