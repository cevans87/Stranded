import concurrent.futures
import dataclasses
import typing

from ..abc import lru_cache_
from ...threading import decorator


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
    future: concurrent.futures.Future[RetT] = dataclasses.field(default_factory=concurrent.futures.Future)

    @typing.override
    def set_value(self, value: Return[RetT] | Raise | Stop) -> None:
        match value:
            case Return(ret=ret): self.future.set_result(ret)
            case Raise() as raise_: self.future.set_exception(raise_.exc_val)
            case Stop() as stop_: self.future.set_exception(stop_)

    @typing.override
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> RetT:
        return self.future.result()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    lru_cache_.Exit[ParamT, RetT, Future[RetT]],
):
    def __call__(self, value: decorator.ValueT[ParamT, RetT], /) -> decorator.StackT:
        match value:
            case Param(): pass
            case Return() | Raise() | Stop(): self.future.set_value(value)

        return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    lru_cache_.Enter[ParamT, RetT, Future[RetT]],
):
    # TODO: Dedup this with the asyncio version.
    def __call__(
        self, value: decorator.ValueT[ParamT, RetT], /,
    ) -> decorator.StackT:
        match value:
            case Param():
                key = self.create_key(*value.args, **value.kwargs)
                future = self.future_by_key.get(key)
                if future is None:
                    while self.decorator.size <= len(self.future_by_key):  # type: ignore[attr-defined]
                        self.future_by_key.popitem(last=False)
                    future = self.future_by_key[key] = self.decorator.future_t()  # type: ignore[attr-defined]
                    return self.exit_t(enter=self, future=future, key=key), self.decoratee  # type: ignore[call-arg, return-value]
                self.future_by_key.move_to_end(key)
                return future,
            case _: return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    lru_cache_.Decorated[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    lru_cache_.Decorator[ParamT, RetT],
):
    decoratee_t: typing.ClassVar = Decoratee
    exit_t: typing.ClassVar = Exit  # type: ignore[assignment]
    enter_t: typing.ClassVar = Enter
    decorated_t: typing.ClassVar = Decorated

    @property
    @typing.override
    def future_t(self) -> type[Future[RetT]]:
        return Future


Decorator = LruCache
lru_cache: LruCache[..., typing.Any] = LruCache()
