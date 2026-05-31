from __future__ import annotations

import abc
import dataclasses
import inspect
import logging
import typing

from ...abc import composer
from ...builtins import exception_


Level = typing.Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']


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
    bound_arguments: inspect.BoundArguments

    def __call__(self, value: composer.ValueT[ParamT, RetT], /) -> composer.StackT:
        match value:
            case Raise() as raise_:
                self.enter.composer.logger.log(  # type: ignore[attr-defined]
                    logging.getLevelNamesMapping()[self.enter.composer.err_level],  # type: ignore[attr-defined]
                    '%s :: %s !! %s',
                    inspect.signature(self.enter.composee),
                    self.bound_arguments.arguments,
                    raise_.exc_val,
                )
            case Return(ret=ret):
                self.enter.composer.logger.log(  # type: ignore[attr-defined]
                    logging.getLevelNamesMapping()[self.enter.composer.ok_level],  # type: ignore[attr-defined]
                    '%s :: %s -> %s',
                    inspect.signature(self.enter.composee),
                    self.bound_arguments.arguments,
                    ret,
                )

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer.Enter[ParamT, RetT], abc.ABC):
    def __call__(self, value: composer.ValueT[ParamT, RetT], /) -> composer.StackT:
        match value:
            case Param() as param_:
                bound_arguments = inspect.signature(self.composee).bind(*param_.args, **param_.kwargs)

                self.composer.logger.log(  # type: ignore[attr-defined]
                    logging.getLevelNamesMapping()[self.composer.call_level],  # type: ignore[attr-defined]
                    '%s',
                    bound_arguments,
                )

                return self.exit_t(enter=self, bound_arguments=bound_arguments), self.composee,  # type: ignore[call-arg]
            case _:
                return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer.Composed[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger[**ParamT, RetT](composer.Composer[ParamT, RetT], abc.ABC):
    logger: logging.Logger
    call_level: Level = 'DEBUG'
    err_level: Level = 'ERROR'
    ok_level: Level = 'INFO'

    Level: typing.ClassVar[type[Level]] = Level  # type: ignore[assignment, valid-type]


Composer = Logger
