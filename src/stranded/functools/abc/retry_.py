from __future__ import annotations

import abc
import dataclasses
import sys
import typing

from ...abc import composer_
from ...builtins import exception_


class Exception(exception_.Exception): ...  # noqa


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], typing.Protocol): ...


Param = composer_.Param
Raise = composer_.Raise
Return = composer_.Return
Stop = composer_.Stop


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer_.Exit[ParamT, RetT], abc.ABC):
    def __call__(self, value: composer_.ValueT[ParamT, RetT], /) -> composer_.StackT:
        if self.enter.n_retried < self.enter.composer.n and isinstance(value, Raise):  # type: ignore[attr-defined]
            return dataclasses.replace(self.enter, n_retried=self.enter.n_retried + 1), self.enter.param  # type: ignore[attr-defined, call-arg]

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], abc.ABC):
    n_retried: int = 0
    param: Param[ParamT] | None = None

    def __call__(self, value: composer_.ValueT[ParamT, RetT], /) -> composer_.StackT:
        match value:
            case Param() as param_:
                new_self = dataclasses.replace(self, param=param_)
                return new_self.composer.Exit(enter=new_self), self.composee
            case _: return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry[**ParamT, RetT](composer_.Composer[ParamT, RetT], abc.ABC):
    n: int = sys.maxsize


Composer = Retry
