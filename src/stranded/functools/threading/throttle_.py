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
class Send[**ParamT, RetT](
    decorator.Send[ParamT, RetT],
    throttle_.Send[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](
    decorator.Receive[ParamT, RetT],
    throttle_.Receive[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    throttle_.Exit[ParamT, RetT],
):
    def __call__(self, result: Raise | RetT) -> tuple[()]:  # type: ignore[override]
        with self.enter.decorated.condition:  # type: ignore[attr-defined]
            return super().__call__(result)  # type: ignore[arg-type]


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    throttle_.Enter[ParamT, RetT],
):
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> tuple[Exit[ParamT, RetT], Decoratee[ParamT, RetT]]:  # type: ignore[override]
        # TODO: this is mostly duplicate with the asyncio version. Try to consolidate.
        state = self.decorated.state  # type: ignore[attr-defined]
        with self.decorated.condition:  # type: ignore[attr-defined]
            if state.num_waiting >= self.decorated.decorator.max_waiting:  # type: ignore[attr-defined]
                raise Exception(f'Exceeded {self.decorated.decorator.max_waiting=}.')  # type: ignore[attr-defined]
            elif 0 < state.num_waiting or state.cap_running <= state.num_running:
                state.num_waiting += 1
                self.decorated.condition.wait_for(lambda: state.num_running < state.cap_running)  # type: ignore[attr-defined]
                state.num_waiting -= 1
            self.decorated.state.num_running += 1  # type: ignore[attr-defined]

        return self.decorated.decorator.exit_t(enter=self), self.decorated.decoratee,  # type: ignore[return-value]


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    throttle_.Decorated[ParamT, RetT, _Condition],
):
    condition: _Condition = dataclasses.field(default_factory=threading.Condition)


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    throttle_.Decorator[ParamT, RetT],
):
    decoratee_t: typing.ClassVar = Decoratee
    receive_t: typing.ClassVar = Receive
    send_t: typing.ClassVar = Send
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    decorated_t: typing.ClassVar = Decorated
Decorator = Throttle
throttle: Throttle[..., typing.Any] = Throttle()
