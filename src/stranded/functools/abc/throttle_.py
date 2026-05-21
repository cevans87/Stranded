from __future__ import annotations

import abc
import dataclasses
import threading
import sys
import typing
import weakref

from ...abc import decorator


class Exception(decorator.Exception): ...  # noqa


@dataclasses.dataclass(kw_only=True)
class State:
    cap_running: int = 1
    num_running: int = 0
    num_waiting: int = 0


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Send[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Receive[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Exit[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    def __call__(self, result: decorator.Raise | RetT) -> ():
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
class Enter[** ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Enter[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT, ConditionT](
    decorator.Decorated[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    condition: ConditionT
    decorated_by_instance: weakref.WeakKeyDictionary[
        decorator.Instance, typing.Self,
    ] = dataclasses.field(default_factory=weakref.WeakKeyDictionary)
    lock: threading.Lock = dataclasses.field(default_factory=threading.Lock)
    state: State = dataclasses.field(default_factory=State)

    def __get__(self, instance, owner) -> typing.Self:
        with self.lock:
            return decorated if (decorated := self.decorated_by_instance.get(instance)) is not None else (
                self.decorated_by_instance.setdefault(
                    instance, dataclasses.replace(
                        self,
                        condition=type(self.condition)(),
                        decoratee=self.decoratee.__get__(instance, owner),
                        state=State(),
                    )
                )
            )


@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorator[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    # How many callees are allowed through concurrently before additional callees become waiters.
    max_running: int = sys.maxsize

    # How many callees are allowed through or to wait concurrently before additional callees are rejected.
    max_waiting: int = sys.maxsize


Decorator = Throttle
throttle = Throttle()
