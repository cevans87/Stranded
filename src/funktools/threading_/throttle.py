import dataclasses
import threading
import typing

from ..abc_ import decorator as abc_decorator
from ..abc_ import throttle as abc_throttle
from . import decorator as threading_decorator


type _Condition[**_Param, _Ret] = threading.Condition
type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Decorator[_Param, _Ret]

type _Ts[**_Param, _Ret] = (
    _Param,
    _Ret,
    _Decoratee[_Param, _Ret],
    _Exit[_Param, _Ret],
    _Enter[_Param, _Ret],
    _Decorated[_Param, _Ret],
    _Decorator[_Param, _Ret],
)


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    threading_decorator.Decoratee[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    abc_throttle.Decoratee[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret](
    threading_decorator.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    abc_throttle.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
):
    def __call__(self, result: abc_decorator.Raise | _Ret) -> ():
        with self.enter.decorated.condition:
            return super().__call__(result)


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret](
    threading_decorator.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    abc_throttle.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
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
    threading_decorator.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    abc_throttle.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Condition[_Param, _Ret],
    ],
):
    condition: _Condition = dataclasses.field(default_factory=threading.Condition)

    @property
    def condition_t(self) -> type[_Condition]:
        return threading.Condition


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret](
    threading_decorator.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    abc_throttle.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...
