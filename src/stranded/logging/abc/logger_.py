from __future__ import annotations

import abc
import dataclasses
import inspect
import logging
import typing

from ...abc import composer_
from ...builtins import exception_


Level = typing.Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']


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
    bound_arguments: inspect.BoundArguments

    def __call__(self, value: composer_.ValueT[ParamT, RetT], /) -> composer_.StackT:
        match value:
            case Raise() as raise_:
                logging.getLogger(f'{self.enter.composee.__module__}.{self.enter.composee.__name__}').log(
                    logging.getLevelNamesMapping()[self.enter.composer.err_level],  # type: ignore[attr-defined]
                    '%s :: %s !! %s',
                    inspect.signature(self.enter.composee),
                    self.bound_arguments.arguments,
                    raise_.exc_val,
                )
            case Return(ret=ret):
                level = self.enter.composer.none_level if ret is None else self.enter.composer.ok_level  # type: ignore[attr-defined]
                logging.getLogger(f'{self.enter.composee.__module__}.{self.enter.composee.__name__}').log(
                    logging.getLevelNamesMapping()[level],
                    '%s :: %s -> %s',
                    inspect.signature(self.enter.composee),
                    self.bound_arguments.arguments,
                    ret,
                )

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], abc.ABC):
    def __call__(self, value: composer_.ValueT[ParamT, RetT], /) -> composer_.StackT:
        match value:
            case Param() as param_:
                bound_arguments = inspect.signature(self.composee).bind(*param_.args, **param_.kwargs)

                logging.getLogger(f'{self.composee.__module__}.{self.composee.__name__}').log(
                    logging.getLevelNamesMapping()[self.composer.call_level],  # type: ignore[attr-defined]
                    '%s',
                    bound_arguments,
                )

                return self.composer.Exit(enter=self, bound_arguments=bound_arguments), self.composee,  # type: ignore[call-arg]
            case _:
                return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger[**ParamT, RetT](composer_.Composer[ParamT, RetT], abc.ABC):
    call_level: Level = 'DEBUG'
    err_level: Level = 'ERROR'
    none_level: Level = 'WARNING'
    ok_level: Level = 'INFO'

    Level: typing.ClassVar[type[Level]] = Level  # type: ignore[assignment, valid-type]


Composer = Logger
