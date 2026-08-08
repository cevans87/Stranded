from __future__ import annotations

import abc
import dataclasses
import threading
import sys
import typing
import weakref

from ...abc import composer_
from ...builtins import exception_


class Exception(exception_.Exception): ...  # noqa


@dataclasses.dataclass(kw_only=True)
class State:
    cap_running: int = 1
    num_running: int = 0
    num_waiting: int = 0


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], typing.Protocol): ...


Param = composer_.Param
Raise = composer_.Raise
Return = composer_.Return
Stop = composer_.Stop


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer_.Exit[ParamT, RetT], abc.ABC):
    def __call__(self, value: composer_.ValueT[ParamT, RetT], /) -> composer_.StackT:
        state = self.enter.state  # type: ignore[attr-defined]
        if isinstance(value, Raise) and state.num_running <= state.cap_running:
            state.cap_running //= 2
        elif (
            not isinstance(value, Raise)
            and state.num_running == state.cap_running < self.enter.composer.max_running  # type: ignore[attr-defined]
        ):
            state.cap_running += 1
        state.num_running -= 1

        if 0 < (n := state.cap_running - state.num_running):
            self.enter.condition.notify(n=n)  # type: ignore[attr-defined]

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], abc.ABC):
    # Per-composition state lives on the Enter now that Enter/Exit no longer reach Composed.
    # Exit reads it back through self.enter; __get__ reinstalls a fresh-state Enter per instance.
    state: State = dataclasses.field(default_factory=State)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], abc.ABC):
    # Enters rather than whole bound compositions: a bound composition holds the bound composee,
    # which refers back to the instance that keys it here, and so would outlive it forever.
    enter_by_instance: weakref.WeakKeyDictionary[
        composer_.Instance, composer_.EnterT[ParamT, RetT],
    ] = dataclasses.field(default_factory=weakref.WeakKeyDictionary)
    lock: threading.Lock = dataclasses.field(default_factory=threading.Lock)

    @typing.override
    def create_enter(self, instance: composer_.Instance) -> composer_.EnterT[ParamT, RetT]:
        with self.lock:
            if (enter := self.enter_by_instance.get(instance)) is not None:
                return enter
            match self.enter:
                case Enter() as enter_:
                    return self.enter_by_instance.setdefault(instance, dataclasses.replace(
                        enter_,
                        condition=type(enter_.condition)(),  # type: ignore[attr-defined]
                        state=State(),
                    ))
            assert False, "unreachable"


@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle[**ParamT, RetT](composer_.Composer[ParamT, RetT], abc.ABC):
    # How many callees are allowed through concurrently before additional callees become waiters.
    max_running: int = sys.maxsize

    # How many callees are allowed through or to wait concurrently before additional callees are rejected.
    max_waiting: int = sys.maxsize


Composer = Throttle
