from __future__ import annotations

import abc
import dataclasses
import sys
import typing

from ...abc import composer
from ...builtins import exception_


class Exception(exception_.Exception): ...  # noqa


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer.Composee[ParamT, RetT], typing.Protocol): ...


Param = composer.Param
Raise = composer.Raise
Return = composer.Return
Stop = composer.Stop


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer.Connect[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer.Exit[ParamT, RetT], abc.ABC):
    def __call__(self, value: composer.ValueT[ParamT, RetT], /) -> composer.StackT:
        if self.enter.n_retried < self.enter.composer.n and isinstance(value, Raise):  # type: ignore[attr-defined]
            return dataclasses.replace(self.enter, n_retried=self.enter.n_retried + 1), self.enter.param  # type: ignore[attr-defined, call-arg]

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer.Enter[ParamT, RetT], abc.ABC):
    n_retried: int = 0
    param: Param[ParamT] | None = None

    def __call__(self, value: composer.ValueT[ParamT, RetT], /) -> composer.StackT:
        match value:
            case Param() as param_:
                new_self = dataclasses.replace(self, param=param_)
                return new_self.exit_t(enter=new_self), self.composee
            case _: return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer.Composed[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry[**ParamT, RetT](composer.Composer[ParamT, RetT], abc.ABC):
    n: int = sys.maxsize


Composer = Retry
