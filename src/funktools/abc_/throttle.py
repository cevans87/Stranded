from __future__ import annotations

import abc
import dataclasses
import threading
import sys
import typing
import weakref

from . import decorator


class Exception(decorator.Exception): ...  # noqa


@dataclasses.dataclass(kw_only=True)
class State:
    cap_running: int = 1
    num_running: int = 0
    num_waiting: int = 0


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator](
    decorator.Exit[_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    def __call__(self, result: decorator.Raise | _Ret) -> ():
        state = self.enter.decorated.state
        if isinstance(result, decorator.Raise) and state.num_running <= state.cap_running:
            state.cap_running //= 2
        elif (
            not isinstance(result, decorator.Raise)
            and state.num_running == state.cap_running < self.enter.decorated.decorator.max_running
        ):
            state.cap_running += 1
        state.num_running -= 1

        if 0 < (n := state.cap_running - state.num_running):
            self.enter.decorated.condition.notify(n=n)

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[** _Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator](
    decorator.Enter[_Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator, _Condition](
    decorator.Decorated[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator],
    abc.ABC,
):
    condition: _Condition
    decorated_by_instance: weakref.WeakKeyDictionary[
        decorator.Instance, typing.Self,
    ] = dataclasses.field(default_factory=weakref.WeakKeyDictionary)
    lock: threading.Lock = dataclasses.field(default_factory=threading.Lock)
    state: State = dataclasses.field(default_factory=State)

    @property
    @abc.abstractmethod
    def condition_t(self) -> type[_Condition]: ...

    def __get__(self, instance, owner) -> typing.Self:
        with self.lock:
            return decorated if (decorated := self.decorated_by_instance.get(instance)) is not None else (
                self.decorated_by_instance.setdefault(
                    instance, dataclasses.replace(
                        self,
                        condition=self.condition_t(),
                        decoratee=self.decoratee.__get__(instance, owner),
                        state=State(),
                    )
                )
            )


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated](
    decorator.Decorator[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
):
    # How many callees are allowed through concurrently before additional callees become waiters.
    max_running: int = sys.maxsize

    # How many callees are allowed through or to wait concurrently before additional callees are rejected.
    max_waiting: int = sys.maxsize

