from __future__ import annotations

import abc
import dataclasses
import sys
import typing

from ...abc import decorator
from ...builtins import exception_


class Exception(exception_.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


Param = decorator.Param
Raise = decorator.Raise
Return = decorator.Return
Stop = decorator.Stop


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    abc.ABC,
):
    def __call__(self, value: decorator.ValueT[ParamT, RetT], /) -> decorator.StackT:
        if self.enter.n_retried < self.enter.decorator.n and isinstance(value, Raise):  # type: ignore[attr-defined]
            return dataclasses.replace(self.enter, n_retried=self.enter.n_retried + 1), self.enter.param  # type: ignore[attr-defined, call-arg]

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    abc.ABC,
):
    n_retried: int = 0
    param: Param[ParamT] | None = None

    def __call__(self, value: decorator.ValueT[ParamT, RetT], /) -> decorator.StackT:
        match value:
            case Param() as param_:
                new_self = dataclasses.replace(self, param=param_)
                return new_self.exit_t(enter=new_self), self.decoratee
            case _: return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    abc.ABC,
): n: int = sys.maxsize


Decorator = Retry
