from __future__ import annotations

import abc
import dataclasses
import inspect
import logging
import typing

from ...funktools.abc_ import decorator


Level = typing.Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']


class Exception(decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**_Param, _Ret, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Decoratee[_Param, _Ret, _Exit, _Enter, _Decorated, _Decorator],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator](
    decorator.Exit[_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    bound_arguments: inspect.BoundArguments

    @abc.abstractmethod
    def __call__(self, result: decorator.Raise | _Ret) -> ():
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
class Enter[** _Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator](
    decorator.Enter[_Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator],
    abc.ABC,
):
    @abc.abstractmethod
    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Exit, _Decoratee]:
        bound_arguments = self.decorated.__signature__.bind(*args, **kwargs)

        self.decorated.decorator.logger.log(
            logging.getLevelNamesMapping()[self.decorated.decorator.call_level],
            '%s',
            bound_arguments,
        )

        return self.decorated.decorator.exit_t(enter=self, bound_arguments=bound_arguments), self.decorated.decoratee,


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator](
    decorator.Decorated[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated](
    decorator.Decorator[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
):
    logger: logging.Logger
    call_level: Level = 'DEBUG'
    err_level: Level = 'ERROR'
    ok_level: Level = 'INFO'
