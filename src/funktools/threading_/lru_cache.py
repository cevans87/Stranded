import concurrent.futures
import dataclasses
import typing

from ..abc_ import lru_cache
from . import decorator


type _Future[**_Param, _Ret] = concurrent.futures.Future[_Ret]
type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Decorator[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[** Param, Ret](lru_cache.Decoratee, decorator.Decoratee, typing.Protocol):

    def __call__(*args: Param.args, **kwargs: Param.kwargs) -> Ret: ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret](
    lru_cache.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Future,
    ],
    decorator.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
):
    future: _Future = dataclasses.field(default_factory=concurrent.futures.Future)

    def __call__(self, result: decorator.Raise | _Ret) -> ():
        self.future.set_result(result)

        return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret](
    lru_cache.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    decorator.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
):
    # TODO: Dedup this with the asyncio version.
    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Decoratee] | tuple[_Exit, _Decoratee]:
        key = self.create_key(*args, **kwargs)
        future = self.decorated.future_by_key.pop(key, None)
        while self.decorated.decorator.size <= len(self.decorated.future_by_key):
            self.decorated.future_by_key.popitem(last=False)
        if future is None:
            future = self.decorated.future_by_key[key] = concurrent.futures.Future()
            return self.decorated.decorator.exit_t(enter=self, future=future), self.decorated.decoratee
        else:
            self.decorated.future_by_key[key] = future
            return (lambda *_args, **_kwargs: future.result()),


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret](
    lru_cache.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Future[_Param, _Ret],
    ],
    decorator.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret](
    lru_cache.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    decorator.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...
