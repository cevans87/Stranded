from __future__ import annotations

import abc
import dataclasses
import sys
import typing

from ...abc import decorator
from ...builtins import exception_


class Exception(exception_.Exception): ...  # noqa


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
    def __call__(self, value: decorator.Param | decorator.Raise | decorator.Return | decorator.Stop) -> tuple[()] | tuple[EnterT, decorator.Param]:
        if self.enter.n_retried < self.enter.decorated.decorator.n and isinstance(value, decorator.Raise):
            return dataclasses.replace(self.enter, n_retried=self.enter.n_retried + 1), self.enter.param

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[** ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Enter[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    n_retried: int = 0
    param: decorator.Param | None = None

    def __call__(self, value: decorator.Param | decorator.Raise | decorator.Return | decorator.Stop) -> tuple[ExitT, DecorateeT] | tuple[()]:
        match value:
            case decorator.Param() as param_:
                new_self = dataclasses.replace(self, param=param_)
                return new_self.exit_t(enter=new_self), self.decorated.decoratee
            case _: return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorated[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorator[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): n: int = sys.maxsize


Decorator = Retry
