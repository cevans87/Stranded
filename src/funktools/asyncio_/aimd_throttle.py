import asyncio
import dataclasses
import typing

from . import decorator
from ..abc_ import aimd_throttle


type _Condition = asyncio.Condition
type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Decorator[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](aimd_throttle.Decoratee, decorator.Decoratee, typing.Protocol):

    async def __call__(*args: _Param.args, **kwargs: _Param.kwargs) -> _Ret: ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret](
    aimd_throttle.Exit[
        _Enter[_Param, _Ret],
        _Ret,
    ],
    decorator.Exit[
        _Enter[_Param, _Ret],
        _Ret,
    ],
):
    async def __call__(self, result: decorator.Raise | _Ret) -> ():
        async with self.enter.decorated.condition:
            return super.__call__(result)


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret](
    aimd_throttle.Enter[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Param,
    ],
    decorator.Enter[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Param,
    ],
):
    async def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Exit, _Decoratee]:
        # TODO: this is mostly duplicate with the threading version. Try to consolidate.
        state = self.decorated.state
        async with self.decorated.condition:
            if state.num_waiting >= self.decorated.decorator.max_waiting:
                raise Exception(f'Exceeded {self.decorated.decorator.max_waiting=}.')
            elif 0 < state.num_waiting or state.cap_running <= state.num_running:
                state.num_waiting += 1
                await self.decorated.condition.wait_for(lambda: state.num_running < state.cap_running)
                state.num_waiting -= 1
            self.decorated.state.num_running += 1

        return self.decorated.decorator.exit_t(enter=self), self.decorated.decoratee,


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret](
    aimd_throttle.Decorated[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Condition,  # FIXME this isn't needed here. It's left over from when condition_t was defined in Decorator
    ],
    decorator.Decorated[
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
        _Param,
        _Ret,
    ],
):
    condition: _Condition = dataclasses.field(default_factory=asyncio.Condition)

    @property
    def condition_t(self) -> type[_Condition]:
        return asyncio.Condition


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret](
    aimd_throttle.Decorator[
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
): ...
