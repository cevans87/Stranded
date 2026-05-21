import dataclasses
import typing

from ..abc import scheduler_
from ...asyncio import decorator


type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Receive[**_Param, _Ret] = Receive[_Param, _Ret]
type _Send[**_Param, _Ret] = Send[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Scheduler[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    scheduler_.Decoratee[_Param, _Ret],
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
    scheduler_.Send[
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
    scheduler_.Receive[
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
    scheduler_.Exit[
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
    scheduler_.Enter[
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
    scheduler_.Decorated[
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
class Scheduler[**_Param, _Ret](
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
    scheduler_.Decorator[
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


Decorator = Scheduler
scheduler = Scheduler()
