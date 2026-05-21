import dataclasses
import typing

from ..abc import get_completion_scheduler_
from ...threading import decorator


type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Receive[**_Param, _Ret] = Receive[_Param, _Ret]
type _Send[**_Param, _Ret] = Send[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = GetCompletionScheduler[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    get_completion_scheduler_.Decoratee[_Param, _Ret],
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
    get_completion_scheduler_.Send[
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
    get_completion_scheduler_.Receive[
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
    get_completion_scheduler_.Exit[
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
): ...


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
    get_completion_scheduler_.Enter[
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
): ...


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
    get_completion_scheduler_.Decorated[
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
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class GetCompletionScheduler[**_Param, _Ret](
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
    get_completion_scheduler_.Decorator[
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
): ...


Decorator = GetCompletionScheduler
get_completion_scheduler = GetCompletionScheduler()
