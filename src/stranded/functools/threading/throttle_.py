import dataclasses
import threading
import typing

from ...threading import decorator
from ..abc import throttle_


type _Condition = threading.Condition


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    throttle_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


Param = decorator.Param
Raise = decorator.Raise
Return = decorator.Return
Stop = decorator.Stop


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    throttle_.Exit[ParamT, RetT],
):
    def __call__(self, value: decorator.ValueT[ParamT, RetT], /) -> decorator.StackT:
        with self.enter.condition:  # type: ignore[attr-defined]
            return super().__call__(value)


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    throttle_.Enter[ParamT, RetT],
):
    condition: _Condition = dataclasses.field(default_factory=threading.Condition)

    def __call__(self, value: decorator.ValueT[ParamT, RetT], /) -> decorator.StackT:  # type: ignore[override]
        # TODO: this is mostly duplicate with the asyncio version. Try to consolidate.
        match value:
            case Param():
                state = self.state
                with self.condition:
                    if state.num_waiting >= self.decorator.max_waiting:  # type: ignore[attr-defined]
                        raise Exception(f'Exceeded {self.decorator.max_waiting=}.')  # type: ignore[attr-defined]
                    elif 0 < state.num_waiting or state.cap_running <= state.num_running:
                        state.num_waiting += 1
                        self.condition.wait_for(lambda: state.num_running < state.cap_running)
                        state.num_waiting -= 1
                    state.num_running += 1

                return self.exit_t(enter=self), self.decoratee,  # type: ignore[return-value]
            case _:
                return ()


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    throttle_.Decorated[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    throttle_.Decorator[ParamT, RetT],
):
    decoratee_t: typing.ClassVar = Decoratee
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    decorated_t: typing.ClassVar = Decorated
Decorator = Throttle
throttle: Throttle[..., typing.Any] = Throttle()
