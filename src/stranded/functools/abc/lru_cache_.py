from __future__ import annotations

import abc
import collections
import dataclasses
import typing
import weakref
import sys

from ...abc import decorator
from ...builtins import exception_


type GenerateKey = typing.Callable[..., Key]
type Key = typing.Hashable


Raise = decorator.Raise
Stop = decorator.Stop
Param = decorator.Param
Return = decorator.Return


class Exception(exception_.Exception): ...  # noqa


@dataclasses.dataclass(frozen=True, kw_only=True)
class Future[RetT](abc.ABC):

    @abc.abstractmethod
    def set_value(self, value: Return[RetT] | Raise | Stop) -> None: ...

    @abc.abstractmethod
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...

    def __get__(self, instance: decorator.Instance, owner: type[object] | None) -> typing.Self:
        return self


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT, FutureT](
    decorator.Exit[ParamT, RetT],
    abc.ABC,
):
    future: FutureT
    key: Key


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT, FutureT](
    decorator.Enter[ParamT, RetT],
    abc.ABC,
):
    # The cache lives on the Enter now that Enter/Exit no longer reach Decorated.
    future_by_key: collections.OrderedDict[Key, FutureT] = dataclasses.field(default_factory=collections.OrderedDict)

    @staticmethod
    def create_key(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Key:
        return tuple(args), tuple(sorted([*kwargs.items()]))


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    abc.ABC,
):
    decorated_by_instance: weakref.WeakKeyDictionary[
        decorator.Instance, typing.Self,
    ] = dataclasses.field(default_factory=weakref.WeakKeyDictionary)

    def __get__(self, instance: decorator.Instance, owner: type[object] | None) -> typing.Self:
        if (decorated := self.decorated_by_instance.get(instance)) is not None:
            return decorated
        match self.stack:
            case [*rest, Enter() as enter_]:
                fresh_enter = dataclasses.replace(
                    enter_,
                    decoratee=enter_.decoratee.__get__(instance, owner),
                    future_by_key=collections.OrderedDict(),
                )
                return self.decorated_by_instance.setdefault(
                    instance, dataclasses.replace(self, stack=(*rest, fresh_enter)),
                )
        assert False, "unreachable"


@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    abc.ABC,
):
    size: int = sys.maxsize

    @property
    @abc.abstractmethod
    def future_t(self) -> type: ...


Decorator = LruCache
