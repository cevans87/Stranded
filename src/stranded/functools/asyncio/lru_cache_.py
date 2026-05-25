import asyncio
import dataclasses
import typing

from ..abc import lru_cache_
from ...asyncio import decorator


Raise = decorator.Raise
Stop = decorator.Stop
Param = decorator.Param
Return = decorator.Return


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    lru_cache_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


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
class Send[**ParamT, RetT](
    decorator.Send[ParamT, RetT],
    lru_cache_.Send[ParamT, RetT, Future[RetT]],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](
    decorator.Receive[ParamT, RetT],
    lru_cache_.Receive[ParamT, RetT, Future[RetT]],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    lru_cache_.Exit[ParamT, RetT, Future[RetT]],
):
    @typing.override
    async def __call__(self, value: Param[ParamT] | Raise | Return[RetT] | Stop) -> tuple[()]:  # type: ignore[override]
        match value:
            case Param(): pass
            case Return() | Raise() | Stop(): self.future.set_value(value)

        return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    lru_cache_.Enter[ParamT, RetT],
):
    # TODO: Dedup this with the threading version.
    @typing.override
    async def __call__(  # type: ignore[override]
        self, value: Param[ParamT] | Raise | Return[RetT] | Stop,
    ) -> tuple[Exit[ParamT, RetT], Decoratee[ParamT, RetT]] | tuple[Future[RetT]] | tuple[()]:
        match value:
            case Param():
                key = self.create_key(*value.args, **value.kwargs)
                future = self.decorated.future_by_key.get(key)  # type: ignore[attr-defined]
                if future is None:
                    while self.decorated.decorator.size <= len(self.decorated.future_by_key):  # type: ignore[attr-defined]
                        self.decorated.future_by_key.popitem(last=False)  # type: ignore[attr-defined]
                    future = self.decorated.future_by_key[key] = self.decorated.decorator.future_t()  # type: ignore[attr-defined]
                    return self.decorated.decorator.exit_t(enter=self, future=future, key=key), self.decorated.decoratee  # type: ignore[call-arg, return-value]
                self.decorated.future_by_key.move_to_end(key)  # type: ignore[attr-defined]
                return future,
            case _: return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    lru_cache_.Decorated[ParamT, RetT, Future[RetT]],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    lru_cache_.Decorator[ParamT, RetT],
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


Decorator = LruCache
lru_cache: LruCache[..., typing.Any] = LruCache()
