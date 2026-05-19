from __future__ import annotations

import abc
import dataclasses
import typing

from ...abc import decorator
from . import operation_state
from . import receiver


class Exception(decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Connect[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Exit[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Enter[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Decorated[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    """The sender instance produced by applying a `Sender` decorator.

    `connect(receiver)` is synchronous — it only constructs an
    `OperationState`. The actual work begins when `start()` is called
    on that operation state, and finishes by invoking exactly one of
    `set_value`/`set_error`/`set_stopped` on the connected receiver.
    """

    @abc.abstractmethod
    def connect(
        self,
        receiver: receiver.Decorated,
        /,
    ) -> operation_state.Decorated: ...

    def __or__(
        self,
        receiver: receiver.Decorated,
    ) -> operation_state.Decorated:
        """`sender | receiver` is sugar for `Connect()(sender, receiver)`."""
        from .. import connect
        return connect.Connect()(self, receiver)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Decorator[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


Sender = Decorator
