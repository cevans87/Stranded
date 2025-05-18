from __future__ import annotations

import abc
import dataclasses
import sys
import typing

from . import decorator


class Exception(decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator](
    decorator.Exit[_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    @abc.abstractmethod
    def __call__(self, result: decorator.Raise | _Ret) -> () | tuple[_Enter]:
        if self.enter.n_retried < self.enter.decorated.decorator.n and isinstance(result, decorator.Raise):
            return dataclasses.replace(self.enter, n_retried=self.enter.n_retried + 1),

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[** _Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator](
    decorator.Enter[_Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator],
    abc.ABC,
): n_retried: int = 0


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator](
    decorator.Decorated[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated](
    decorator.Decorator[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
): n: int = sys.maxsize
