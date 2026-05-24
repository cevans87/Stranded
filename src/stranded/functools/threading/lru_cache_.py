import concurrent.futures
import dataclasses
import typing

from ..abc import lru_cache_
from ...threading import decorator


type _Decoratee[**ParamT, RetT] = Decoratee[ParamT, RetT]
type _Receive[**ParamT, RetT] = Receive[ParamT, RetT]
type _Send[**ParamT, RetT] = Send[ParamT, RetT]
type _Exit[**ParamT, RetT] = Exit[ParamT, RetT]
type _Enter[**ParamT, RetT] = Enter[ParamT, RetT]
type _Decorated[**ParamT, RetT] = Decorated[ParamT, RetT]
type _Decorator[**ParamT, RetT] = LruCache[ParamT, RetT]
type _Future[RetT] = Future[RetT]


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
class Send[**ParamT, RetT](
    decorator.Send[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
    ],
    lru_cache_.Send[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
        _Future[RetT],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](
    decorator.Receive[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
    ],
    lru_cache_.Receive[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
        _Future[RetT],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
    ],
    lru_cache_.Exit[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
        _Future[RetT],
    ],
):
    def __call__(self, value: Param[ParamT] | Raise | Return[RetT] | Stop) -> tuple[()]:
        match value:
            case Param(): pass
            case Return() | Raise() | Stop(): self.future.set_value(value)

        return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
    ],
    lru_cache_.Enter[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
    ],
):
    # TODO: Dedup this with the asyncio version.
    def __call__(
        self, value: Param[ParamT] | Raise | Return[RetT] | Stop,
    ) -> tuple[_Exit[ParamT, RetT], _Decoratee[ParamT, RetT]] | tuple[_Future[RetT]] | tuple[()]:
        match value:
            case Param():
                key = self.create_key(*value.args, **value.kwargs)
                future = self.decorated.future_by_key.get(key)
                if future is None:
                    while self.decorated.decorator.size <= len(self.decorated.future_by_key):
                        self.decorated.future_by_key.popitem(last=False)
                    future = self.decorated.future_by_key[key] = self.decorated.decorator.future_t()
                    return self.exit_t(enter=self, future=future, key=key), self.decorated.decoratee
                self.decorated.future_by_key.move_to_end(key)
                return future,
            case _: return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
    ],
    lru_cache_.Decorated[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
        _Future[RetT],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache[**ParamT, RetT](
    decorator.Decorator[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
    ],
    lru_cache_.Decorator[
        ParamT,
        RetT,
        _Decoratee[ParamT, RetT],
        _Receive[ParamT, RetT],
        _Send[ParamT, RetT],
        _Exit[ParamT, RetT],
        _Enter[ParamT, RetT],
        _Decorated[ParamT, RetT],
        _Decorator[ParamT, RetT],
    ],
):
    @property
    @typing.override
    def future_t(self) -> type[_Future[RetT]]:
        return Future


Decorator = LruCache
lru_cache: LruCache[..., typing.Any] = LruCache()