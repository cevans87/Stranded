from __future__ import annotations

import abc
import annotated_types
import dataclasses
import sys
import typing

from . import decorator


class Exception(decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee(decorator.Decoratee, typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[_Enter, _Ret](decorator.Exit[_Enter, _Ret], abc.ABC):

    @abc.abstractmethod
    def __call__(self, result: decorator.Raise | _Ret) -> ():
        if self.enter.n_retried < self.enter.decorated.decorator.n and isinstance(result, decorator.Raise):
            return dataclasses.replace(self.enter, n_retried=self.enter.n_retried + 1),

        return result,


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[_Decoratee, _Exit, _Decorated, **_Param](
    decorator.Enter[_Decoratee, _Exit, _Decorated, _Param],
    abc.ABC,
):
    n_retried: int = 0


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
    n: typing.Annotated[int, annotated_types.Ge(0)] = sys.maxsize
