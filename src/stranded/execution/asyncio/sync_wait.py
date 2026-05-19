import dataclasses
import typing

from ..abc import sync_wait
from ..stopped import Stopped
from . import receiver
from ...asyncio import decorator


type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Connect[**_Param, _Ret] = Connect[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Decorator[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    sync_wait.Decoratee[_Param, _Ret],
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
    sync_wait.Connect[
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
    sync_wait.Exit[
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
    sync_wait.Enter[
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
    receiver.Decorated[_Param, _Ret],
    sync_wait.Decorated[
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
    """Async SyncWait IS-A Receiver: connects the wrapped sender to itself,
    awaits the resulting op state's start, and reads the completion back
    out of its own state. Single-shot per `__call__`."""

    state: dict[str, typing.Any] = dataclasses.field(default_factory=dict)

    async def set_value(self, *values: typing.Any) -> None:
        self.state['value'] = values

    async def set_error(self, err: BaseException) -> None:
        self.state['error'] = err

    async def set_stopped(self) -> None:
        self.state['stopped'] = True

    async def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> _Ret:
        self.state.clear()
        await self.decoratee.connect(self).start()
        if 'error' in self.state:
            raise self.state['error']
        if self.state.get('stopped'):
            raise Stopped
        return self.state['value']


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
    sync_wait.Decorator[
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


SyncWait = Decorator
