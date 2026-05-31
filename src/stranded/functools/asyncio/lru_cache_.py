import asyncio
import dataclasses
import typing

from ..abc import lru_cache_
from ...asyncio import composer


Raise = composer.Raise
Stop = composer.Stop
Param = composer.Param
Return = composer.Return


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer.Composee[ParamT, RetT], lru_cache_.Composee[ParamT, RetT], typing.Protocol): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Future[RetT](lru_cache_.Future[RetT]):
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
class Connect[**ParamT, RetT](composer.Connect[ParamT, RetT], lru_cache_.Connect[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer.Exit[ParamT, RetT], lru_cache_.Exit[ParamT, RetT, Future[RetT]]):
    @typing.override
    async def __call__(self, value: composer.ValueT[ParamT, RetT], /) -> composer.StackT:  # type: ignore[override]
        match value:
            case Param(): pass
            case Return() | Raise() | Stop(): self.future.set_value(value)

        return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer.Enter[ParamT, RetT], lru_cache_.Enter[ParamT, RetT, Future[RetT]]):
    # TODO: Dedup this with the threading version.
    @typing.override
    async def __call__(  # type: ignore[override]
        self, value: composer.ValueT[ParamT, RetT], /,
    ) -> composer.StackT:
        match value:
            case Param():
                key = self.create_key(*value.args, **value.kwargs)
                future = self.future_by_key.get(key)
                if future is None:
                    while self.composer.size <= len(self.future_by_key):  # type: ignore[attr-defined]
                        self.future_by_key.popitem(last=False)
                    future = self.future_by_key[key] = self.composer.future_t()  # type: ignore[attr-defined]
                    return self.exit_t(enter=self, future=future, key=key), self.composee  # type: ignore[call-arg, return-value]
                self.future_by_key.move_to_end(key)
                return future,
            case _: return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer.Composed[ParamT, RetT], lru_cache_.Composed[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache[**ParamT = ..., RetT = typing.Any](composer.Composer[ParamT, RetT], lru_cache_.Composer[ParamT, RetT]):
    composee_t: typing.ClassVar = Composee
    connect_t: typing.ClassVar = Connect
    exit_t: typing.ClassVar = Exit  # type: ignore[assignment]
    enter_t: typing.ClassVar = Enter
    composed_t: typing.ClassVar = Composed

    @property
    @typing.override
    def future_t(self) -> type[Future[RetT]]:
        return Future


Composer = LruCache
lru_cache = LruCache()
