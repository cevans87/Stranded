import dataclasses
import threading
import typing

import boltins.decorator.threading as decorator
from . import _common as common


type _Condition[**_Param, _Ret] = threading.Condition
type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Decorator[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[** Param, Ret](common.Decoratee, decorator.Decoratee, typing.Protocol):

    def __call__(*args: Param.args, **kwargs: Param.kwargs) -> Ret: ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret](
    common.Exit[
        _Enter[_Param, _Ret],
        _Ret,
    ],
    decorator.Exit[
        _Enter[_Param, _Ret],
        _Ret,
    ],
):
    def __call__(self, result: decorator.Raise | _Ret) -> ():
        with self.enter.decorated.condition:
            return super().__call__(result)


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret](
    common.Enter[
        _Decorated[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Param,
    ],
    decorator.Enter[
        _Decoratee[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Param,
    ],
):
    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Exit, _Decoratee]:
        # TODO: this is mostly duplicate with the asyncio version. Try to consolidate.
        state = self.decorated.state
        with self.decorated.condition:
            if state.num_waiting >= self.decorated.decorator.max_waiting:
                raise Exception(f'Exceeded {self.decorated.decorator.max_waiting=}.')
            elif 0 < state.num_waiting or state.cap_running <= state.num_running:
                state.num_waiting += 1
                self.decorated.condition.wait_for(lambda: state.num_running < state.cap_running)
                state.num_waiting -= 1
            self.decorated.state.num_running += 1

        return self.decorated.decorator.exit_t(enter=self), self.decorated.decoratee,


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret](
    common.Decorated[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Condition,
    ],
    decorator.Decorated[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Param,
        _Ret,
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret](
    common.Decorator[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Condition,
    ],
    decorator.Decorator[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
):
    @property
    def condition_t(self) -> type[_Condition]:
        return threading.Condition
