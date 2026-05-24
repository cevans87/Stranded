import dataclasses
import typing

from ..abc import start_
from ...threading import decorator


type _Decoratee[**ParamT, RetT] = Decoratee[ParamT, RetT]
type _Receive[**ParamT, RetT] = Receive[ParamT, RetT]
type _Send[**ParamT, RetT] = Send[ParamT, RetT]
type _Exit[**ParamT, RetT] = Exit[ParamT, RetT]
type _Enter[**ParamT, RetT] = Enter[ParamT, RetT]
type _Decorated[**ParamT, RetT] = Decorated[ParamT, RetT]
type _Decorator[**ParamT, RetT] = Start[ParamT, RetT]


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    start_.Decoratee[ParamT, RetT],
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
    start_.Send[
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
    start_.Receive[
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
    start_.Exit[
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
    start_.Enter[
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
    start_.Decorated[
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
class Start[**ParamT, RetT](
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
    start_.Decorator[
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


Decorator = Start
start: Start[..., typing.Any] = Start()