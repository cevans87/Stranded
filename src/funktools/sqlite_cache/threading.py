import concurrent.futures
import dataclasses
import typing

import boltins.decorator.threading as decorator
from . import _common as common


type _Future[**_Param, _Ret] = concurrent.futures.Future[_Ret]
type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Decorator[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[** Param, Ret](common.Decoratee, decorator.Decoratee, typing.Protocol):

    def __call__(*args: Param.args, **kwargs: Param.kwargs) -> Ret: ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret](
    common.Exit[
        _Enter[_Param, _Ret],
        _Future[_Param, _Ret],
    ],
    decorator.Exit[
        _Enter[_Param, _Ret],
        _Ret,
    ],
):
    future: _Future = dataclasses.field(default_factory=concurrent.futures.Future)

    def __call__(self, result: decorator.Raise | _Ret) -> ():
        self.future.set_result(result)

        return tuple()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret](
    common.Enter[
        _Decorated[_Param, _Ret],
    ],
    decorator.Enter[
        _Decoratee[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Param,
    ],
):
    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Decoratee] | tuple[_Exit, _Decoratee]:
        key = self.decorated.decorator.generate_key(*args, **kwargs)

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
    common.Decorated[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Future[_Param, _Ret],
    ],
    decorator.Decorated[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Param,
        _Ret,
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret](
    common.Decorator[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    decorator.Decorator[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...
