import dataclasses
import typing

import boltins.decorator.threading as decorator
from . import _common as common


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
        _Ret,
    ],
    decorator.Exit[
        _Enter[_Param, _Ret],
        _Ret,
    ],
):
    def __call__(self, result: decorator.Raise | _Ret) -> ():
        return super().__call__(result)


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret](
    common.Enter[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Param,
    ],
    decorator.Enter[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Param,
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret](
    common.Decorated[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
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
