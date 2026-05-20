import dataclasses
import typing

from ..abc import when_all_with_variant
from ...threading import decorator


type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Receive[**_Param, _Ret] = Receive[_Param, _Ret]
type _Send[**_Param, _Ret] = Send[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Decorator[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    when_all_with_variant.Decoratee[_Param, _Ret],
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
    when_all_with_variant.Send[
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
    when_all_with_variant.Receive[
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
    when_all_with_variant.Exit[
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
    when_all_with_variant.Enter[
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
    when_all_with_variant.Decorated[
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
class Decorator[**_Param, _Ret](
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
    when_all_with_variant.Decorator[
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


WhenAllWithVariant = Decorator
