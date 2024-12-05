from __future__ import annotations

import abc
import dataclasses
import inspect
import logging
import typing

from . import decorator


Level = typing.Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']


class Exception(Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee(decorator.Decoratee, typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[_Enter, _Ret](decorator.Exit[_Enter], abc.ABC):

    @abc.abstractmethod
    def __call__(self, result: decorator.Raise | _Ret) -> ():
        return tuple()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[_Decoratee, _Exit, _Decorated, **_Param](
    decorator.Enter[_Decoratee, _Exit, _Decorated, _Param],
    abc.ABC,
):

    @abc.abstractmethod
    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Exit, _Decoratee]:
        bound_arguments = self.decorated.__signature__.bind(*args, **kwargs)

        self.decorated.base.logger.log(
            logging.getLevelNamesMapping()[self.decorated.base.call_level],
            '%s',
            bound_arguments,
        )

        return self.decorated.base.exit_t(enter=self, bound_arguments=bound_arguments), self.decorated.decoratee,



@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[_Decoratee, _Exit, _Enter, _Decorator](
    decorator.Decorated[_Decoratee, _Exit, _Enter, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[_Decoratee, _Exit, _Enter, _Decorated](
    decorator.Decorator[_Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
):
    logger: logging.Logger
    call_level: Level = 'DEBUG'
    err_level: Level = 'ERROR'
    ok_level: Level = 'INFO'
