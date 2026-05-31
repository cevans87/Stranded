from __future__ import annotations

import abc
import dataclasses
import threading
import sys
import typing
import weakref

from ...abc import composer
from ...builtins import exception_


class Exception(exception_.Exception): ...  # noqa


@dataclasses.dataclass(kw_only=True)
class State:
    cap_running: int = 1
    num_running: int = 0
    num_waiting: int = 0


@typing.runtime_checkable
class Composee[**ParamT, RetT](
    composer.Composee[ParamT, RetT],
    typing.Protocol,
): ...


Param = composer.Param
Raise = composer.Raise
Return = composer.Return
Stop = composer.Stop


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](
    composer.Connect[ParamT, RetT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    composer.Exit[ParamT, RetT],
    abc.ABC,
):
    def __call__(self, value: composer.ValueT[ParamT, RetT], /) -> composer.StackT:
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
class Enter[**ParamT, RetT](
    composer.Enter[ParamT, RetT],
    abc.ABC,
):
    # Per-composition state lives on the Enter now that Enter/Exit no longer reach Composed.
    # Exit reads it back through self.enter; __get__ reinstalls a fresh-state Enter per instance.
    state: State = dataclasses.field(default_factory=State)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](
    composer.Composed[ParamT, RetT],
    abc.ABC,
):
    composed_by_instance: weakref.WeakKeyDictionary[
        composer.Instance, typing.Self,
    ] = dataclasses.field(default_factory=weakref.WeakKeyDictionary)
    lock: threading.Lock = dataclasses.field(default_factory=threading.Lock)

    def __get__(self, instance: composer.Instance, owner: type[object] | None) -> typing.Self:
        with self.lock:
            if (composed := self.composed_by_instance.get(instance)) is not None:
                return composed
            match self.stack:
                case [*rest, Enter() as enter_]:
                    fresh_enter = dataclasses.replace(
                        enter_,
                        condition=type(enter_.condition)(),  # type: ignore[attr-defined]
                        composee=enter_.composee.__get__(instance, owner),
                        state=State(),
                    )
                    return self.composed_by_instance.setdefault(
                        instance, dataclasses.replace(self, stack=(*rest, fresh_enter)),
                    )
            assert False, "unreachable"


@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle[**ParamT, RetT](
    composer.Composer[ParamT, RetT],
    abc.ABC,
):
    # How many callees are allowed through concurrently before additional callees become waiters.
    max_running: int = sys.maxsize

    # How many callees are allowed through or to wait concurrently before additional callees are rejected.
    max_waiting: int = sys.maxsize


Composer = Throttle
