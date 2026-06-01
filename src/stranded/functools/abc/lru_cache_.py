from __future__ import annotations

import abc
import collections
import dataclasses
import typing
import weakref
import sys

from ...abc import composer
from ...builtins import exception_


type GenerateKey = typing.Callable[..., Key]
type Key = typing.Hashable


Raise = composer.Raise
Stop = composer.Stop
Param = composer.Param
Return = composer.Return


class Exception(exception_.Exception): ...  # noqa


@dataclasses.dataclass(frozen=True, kw_only=True)
class Future[RetT](abc.ABC):

    @abc.abstractmethod
    def set_value(self, value: Return[RetT] | Raise | Stop) -> None: ...

    @abc.abstractmethod
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...

    def __get__(self, instance: composer.Instance, owner: type[object] | None) -> typing.Self:
        return self


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer.Composee[ParamT, RetT], typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer.Connect[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT, FutureT](composer.Exit[ParamT, RetT], abc.ABC):
    future: FutureT
    key: Key


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT, FutureT](composer.Enter[ParamT, RetT], abc.ABC):
    future_by_key: collections.OrderedDict[Key, FutureT] = dataclasses.field(default_factory=collections.OrderedDict)

    @staticmethod
    def create_key(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Key:
        return tuple(args), tuple(sorted([*kwargs.items()]))


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer.Composed[ParamT, RetT], abc.ABC):
    composed_by_instance: weakref.WeakKeyDictionary[
        composer.Instance, typing.Self,
    ] = dataclasses.field(default_factory=weakref.WeakKeyDictionary)

    def __get__(self, instance: composer.Instance, owner: type[object] | None) -> typing.Self:
        if (composed := self.composed_by_instance.get(instance)) is not None:
            return composed
        match self.stack[-1]:
            case Enter() as enter_:
                return self.composed_by_instance.setdefault(
                    instance, dataclasses.replace(
                        self,
                        stack=(
                            *self.stack[:-1],
                            dataclasses.replace(
                                enter_,
                                composee=enter_.composee.__get__(instance, owner),
                                future_by_key=collections.OrderedDict(),
                            )
                        )
                    ),
                )
        assert False, "unreachable"


@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache[**ParamT, RetT](composer.Composer[ParamT, RetT], abc.ABC):
    size: int = sys.maxsize

    @property
    @abc.abstractmethod
    def future_t(self) -> type: ...


Composer = LruCache
