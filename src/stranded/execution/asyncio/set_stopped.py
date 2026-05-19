import dataclasses
import typing

from ..abc import set_stopped
from ...asyncio import decorator


type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Connect[**_Param, _Ret] = Connect[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Decorator[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    set_stopped.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**_Param, _Ret](
    decorator.Connect[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    set_stopped.Connect[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret](
    decorator.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    set_stopped.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret](
    decorator.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    set_stopped.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret](
    decorator.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    set_stopped.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret](
    decorator.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    set_stopped.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


SetStopped = Decorator
