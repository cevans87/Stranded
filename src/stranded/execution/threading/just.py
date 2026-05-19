import dataclasses
import typing

from ..abc import just
from ..stopped import Stopped
from . import operation_state
from . import receiver
from . import sender
from ...threading import decorator


type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Connect[**_Param, _Ret] = Connect[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Decorator[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    just.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**_Param, _Ret](
    decorator.Connect[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    just.Connect[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret](
    decorator.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    just.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret](
    decorator.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    just.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret](
    sender.Decorated[_Param, _Ret],
    just.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
):
    def connect(
        self,
        receiver: receiver.Decorated,
        /,
    ) -> operation_state.Decorated:
        produce = self.decoratee

        def _thunk() -> None:
            try:
                value = produce()
            except Stopped:
                receiver.set_stopped()
            except Exception as exc:  # noqa: BLE001
                receiver.set_error(exc)
            else:
                receiver.set_value(value)

        return operation_state.Decorator()(_thunk)


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret](
    decorator.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    just.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Connect[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


Just = Decorator
