import dataclasses
import typing

from ..abc import set_value_
from ...asyncio import decorator


type _Decoratee[**ParamT, RetT] = Decoratee[ParamT, RetT]
type _Receive[**ParamT, RetT] = Receive[ParamT, RetT]
type _Send[**ParamT, RetT] = Send[ParamT, RetT]
type _Exit[**ParamT, RetT] = Exit[ParamT, RetT]
type _Enter[**ParamT, RetT] = Enter[ParamT, RetT]
type _Decorated[**ParamT, RetT] = Decorated[ParamT, RetT]
type _Decorator[**ParamT, RetT] = SetValue[ParamT, RetT]


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    set_value_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


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
    set_value_.Send[
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
    set_value_.Receive[
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
    set_value_.Exit[
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
): ...


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
    set_value_.Enter[
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
): ...


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
    set_value_.Decorated[
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
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class SetValue[**ParamT, RetT](
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
    set_value_.Decorator[
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
): ...


Decorator = SetValue
set_value: SetValue[..., typing.Any] = SetValue()