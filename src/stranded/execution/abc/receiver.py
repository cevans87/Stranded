from __future__ import annotations

import abc
import dataclasses
import typing

from ...abc import decorator


class Exception(decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Connect[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Exit[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Enter[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Decorated[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    """The receiver instance produced by applying a `Receiver` decorator.

    Exactly one of `set_value`, `set_error`, `set_stopped` will be
    delivered by the connected sender.
    """

    @abc.abstractmethod
    def set_value(self, *values: typing.Any) -> typing.Any: ...

    @abc.abstractmethod
    def set_error(self, err: BaseException) -> typing.Any: ...

    @abc.abstractmethod
    def set_stopped(self) -> typing.Any: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Decorator[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


Receiver = Decorator
