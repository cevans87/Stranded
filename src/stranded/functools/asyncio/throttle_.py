import asyncio
import dataclasses
import typing

from ..abc import throttle_
from ...asyncio import composer

type _Condition = asyncio.Condition


@typing.runtime_checkable
class Composee[**ParamT, RetT](
    composer.Composee[ParamT, RetT],
    throttle_.Composee[ParamT, RetT],
    typing.Protocol,
): ...


Param = composer.Param
Raise = composer.Raise
Return = composer.Return
Stop = composer.Stop


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](
    composer.Connect[ParamT, RetT],
    throttle_.Connect[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    composer.Exit[ParamT, RetT],
    throttle_.Exit[ParamT, RetT],
):
    async def __call__(self, value: composer.ValueT[ParamT, RetT], /) -> composer.StackT:  # type: ignore[override]
        async with self.enter.condition:  # type: ignore[attr-defined]
            return await super().__call__(value)


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    composer.Enter[ParamT, RetT],
    throttle_.Enter[ParamT, RetT],
):
    condition: _Condition = dataclasses.field(default_factory=asyncio.Condition)

    async def __call__(self, value: composer.ValueT[ParamT, RetT], /) -> composer.StackT:  # type: ignore[override]
        # TODO: this is mostly duplicate with the threading version. Try to consolidate.
        match value:
            case Param():
                state = self.state
                async with self.condition:
                    if state.num_waiting >= self.composer.max_waiting:  # type: ignore[attr-defined]
                        raise Exception(f'Exceeded {self.composer.max_waiting=}.')  # type: ignore[attr-defined]
                    elif 0 < state.num_waiting or state.cap_running <= state.num_running:
                        state.num_waiting += 1
                        await self.condition.wait_for(lambda: state.num_running < state.cap_running)
                        state.num_waiting -= 1
                    state.num_running += 1

                return self.exit_t(enter=self), self.composee,  # type: ignore[return-value]
            case _:
                return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](
    composer.Composed[ParamT, RetT],
    throttle_.Composed[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle[**ParamT, RetT](
    composer.Composer[ParamT, RetT],
    throttle_.Composer[ParamT, RetT],
):
    composee_t: typing.ClassVar = Composee
    connect_t: typing.ClassVar = Connect
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    composed_t: typing.ClassVar = Composed
Composer = Throttle
throttle: Throttle[..., typing.Any] = Throttle()
