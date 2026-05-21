from __future__ import annotations

import abc
import dataclasses
import inspect
import logging
import typing

from ...abc import decorator


Level = typing.Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']


class Exception(decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Send[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Receive[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Exit[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    bound_arguments: inspect.BoundArguments

    @abc.abstractmethod
    def __call__(self, result: decorator.Raise | RetT) -> ():
        if isinstance(result, decorator.Raise):
            self.enter.decorated.decorator.logger.log(
                logging.getLevelNamesMapping()[self.enter.decorated.decorator.err_level],
                '%s :: %s !! %s',
                self.enter.decorated.__signature__,
                self.bound_arguments.arguments,
                result.exc_val,
            )
        else:
            self.enter.decorated.decorator.logger.log(
                logging.getLevelNamesMapping()[self.enter.decorated.decorator.ok_level],
                '%s :: %s -> %s',
                self.enter.decorated.__signature__,
                self.bound_arguments.arguments,
                result,
            )

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[** ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Enter[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    @abc.abstractmethod
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> tuple[ExitT, DecorateeT]:
        bound_arguments = self.decorated.__signature__.bind(*args, **kwargs)

        self.decorated.decorator.logger.log(
            logging.getLevelNamesMapping()[self.decorated.decorator.call_level],
            '%s',
            bound_arguments,
        )

        return self.decorated.decorator.exit_t(enter=self, bound_arguments=bound_arguments), self.decorated.decoratee,


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorated[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorator[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    logger: logging.Logger
    call_level: Level = 'DEBUG'
    err_level: Level = 'ERROR'
    ok_level: Level = 'INFO'

    Level: typing.ClassVar[type[Level]] = Level


Decorator = Logger
