from __future__ import annotations

import abc
import collections
import dataclasses
import typing
import weakref
import sys

from . import decorator as abc_decorator


type GenerateKey = typing.Callable[..., Key]
type Key = typing.Hashable


class Exception(abc_decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**_Param, _Ret, _Decoratee: typing.Self, _Exit, _Enter, _Decorated, _Decorator](
    abc_decorator.Decoratee[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Exit: typing.Self, _Enter, _Decorated, _Decorator, _Future](
    abc_decorator.Exit[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): future: _Future


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret, _Decoratee, _Exit, _Enter: typing.Self, _Decorated, _Decorator](
    abc_decorator.Enter[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    @staticmethod
    def create_key(*args: _Param.args, **kwargs: _Param.kwargs) -> Key:
        return tuple(args), tuple(sorted([*kwargs.items()]))


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated: typing.Self, _Decorator, _Future](
    abc_decorator.Decorated[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    decorated_by_instance: weakref.WeakKeyDictionary[
        abc_decorator.Instance, typing.Self,
    ] = dataclasses.field(default_factory=weakref.WeakKeyDictionary)
    future_by_key: collections.OrderedDict[Key, _Future] = dataclasses.field(default_factory=collections.OrderedDict)

    def __get__(self, instance, owner) -> typing.Self:
        return decorated if (decorated := self.decorated_by_instance.get(instance)) is not None else (
            self.decorated_by_instance.setdefault(
                instance, dataclasses.replace(
                    self,
                    decoratee=self.decoratee.__get__(instance, owner),
                    future_by_key=collections.OrderedDict(),
                )
            )
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator: typing.Self](
    abc_decorator.Decorator[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): size: int = sys.maxsize
