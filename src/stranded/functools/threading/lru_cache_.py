import concurrent.futures
import dataclasses
import typing

from . import herd_
from ..abc import lru_cache_
from ...threading import decorator


type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Receive[**_Param, _Ret] = Receive[_Param, _Ret]
type _Send[**_Param, _Ret] = Send[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = LruCache[_Param, _Ret]
type _Future[_Ret] = concurrent.futures.Future[_Ret]


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    lru_cache_.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**_Param, _Ret](
    decorator.Send[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    lru_cache_.Send[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Future[_Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**_Param, _Ret](
    decorator.Receive[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    lru_cache_.Receive[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Future[_Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret](
    decorator.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    lru_cache_.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Future[_Ret],
    ],
):
    def __call__(self, result: decorator.Raise | _Ret) -> tuple[()]:
        future_by_key = self.enter.decorated.future_by_key
        while self.enter.decorated.decorator.size <= len(future_by_key):
            future_by_key.popitem(last=False)
        future = concurrent.futures.Future()
        future.set_result(result)
        future_by_key[self.key] = future

        return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret](
    decorator.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    lru_cache_.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
):
    # TODO: Dedup this with the asyncio version.
    def __call__(
        self, *args: _Param.args, **kwargs: _Param.kwargs,
    ) -> tuple[_Exit[_Param, _Ret], _Decoratee[_Param, _Ret]] | tuple[typing.Callable[_Param, _Ret]]:
        key = self.create_key(*args, **kwargs)
        future = self.decorated.future_by_key.get(key)
        match future is None:
            case True:
                return self.exit_t(enter=self, key=key), self.decorated.decoratee
            case False:
                self.decorated.future_by_key.move_to_end(key)
                return (lambda *_args, **_kwargs: future.result()),
        assert False, "Unreachable"


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret](
    decorator.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    lru_cache_.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Future[_Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache[**_Param, _Ret](
    decorator.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    lru_cache_.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Receive[_Param, _Ret],
        _Send[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
):
    @typing.override
    def __call__(self, decoratee: _Decoratee[_Param, _Ret], /) -> _Decorated[_Param, _Ret]:
        return super().__call__(herd_.Herd()(decoratee))


Decorator = LruCache
lru_cache = LruCache()
