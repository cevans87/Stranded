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
class Send[**ParamT, RetT](
    decorator.Send[ParamT, RetT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](
    decorator.Receive[ParamT, RetT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    abc.ABC,
):
    bound_arguments: inspect.BoundArguments

    @abc.abstractmethod
    def __call__(self, result: Raise | RetT) -> tuple[()]:  # type: ignore[override]
        if isinstance(result, Raise):
            self.enter.decorated.decorator.logger.log(  # type: ignore[attr-defined]
                logging.getLevelNamesMapping()[self.enter.decorated.decorator.err_level],  # type: ignore[attr-defined]
                '%s :: %s !! %s',
                self.enter.decorated.__signature__,
                self.bound_arguments.arguments,
                result.exc_val,
            )
        else:
            self.enter.decorated.decorator.logger.log(  # type: ignore[attr-defined]
                logging.getLevelNamesMapping()[self.enter.decorated.decorator.ok_level],  # type: ignore[attr-defined]
                '%s :: %s -> %s',
                self.enter.decorated.__signature__,
                self.bound_arguments.arguments,
                result,
            )

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    abc.ABC,
):
    @abc.abstractmethod
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> tuple[Exit[ParamT, RetT], Decoratee[ParamT, RetT]]:  # type: ignore[override]
        bound_arguments = self.decorated.__signature__.bind(*args, **kwargs)

        self.decorated.decorator.logger.log(  # type: ignore[attr-defined]
            logging.getLevelNamesMapping()[self.decorated.decorator.call_level],  # type: ignore[attr-defined]
            '%s',
            bound_arguments,
        )

        return self.decorated.decorator.exit_t(enter=self, bound_arguments=bound_arguments), self.decorated.decoratee,  # type: ignore[call-arg, return-value]


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
