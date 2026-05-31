from __future__ import annotations

import abc
import dataclasses
import inspect
import logging
import typing

from ...abc import decorator
from ...builtins import exception_


Level = typing.Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']


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
    bound_arguments: inspect.BoundArguments

    def __call__(self, value: decorator.ValueT[ParamT, RetT], /) -> decorator.StackT:
        match value:
            case Raise() as raise_:
                self.enter.decorator.logger.log(  # type: ignore[attr-defined]
                    logging.getLevelNamesMapping()[self.enter.decorator.err_level],  # type: ignore[attr-defined]
                    '%s :: %s !! %s',
                    inspect.signature(self.enter.decoratee),
                    self.bound_arguments.arguments,
                    raise_.exc_val,
                )
            case Return(ret=ret):
                self.enter.decorator.logger.log(  # type: ignore[attr-defined]
                    logging.getLevelNamesMapping()[self.enter.decorator.ok_level],  # type: ignore[attr-defined]
                    '%s :: %s -> %s',
                    inspect.signature(self.enter.decoratee),
                    self.bound_arguments.arguments,
                    ret,
                )

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    abc.ABC,
):
    def __call__(self, value: decorator.ValueT[ParamT, RetT], /) -> decorator.StackT:
        match value:
            case Param() as param_:
                bound_arguments = inspect.signature(self.decoratee).bind(*param_.args, **param_.kwargs)

                self.decorator.logger.log(  # type: ignore[attr-defined]
                    logging.getLevelNamesMapping()[self.decorator.call_level],  # type: ignore[attr-defined]
                    '%s',
                    bound_arguments,
                )

                return self.exit_t(enter=self, bound_arguments=bound_arguments), self.decoratee,  # type: ignore[call-arg]
            case _:
                return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    abc.ABC,
):
    logger: logging.Logger
    call_level: Level = 'DEBUG'
    err_level: Level = 'ERROR'
    ok_level: Level = 'INFO'

    Level: typing.ClassVar[type[Level]] = Level  # type: ignore[assignment, valid-type]


Decorator = Logger
