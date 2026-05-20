from __future__ import annotations

import abc
import collections
import dataclasses
import typing
import weakref
import sys

from ...abc import decorator


type GenerateKey = typing.Callable[..., Key]
type Key = typing.Hashable


class Exception(decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator, _Future](
    decorator.Send[_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator, _Future](
    decorator.Receive[_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator, _Future](
    decorator.Exit[_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): future: _Future


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Enter[_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    @staticmethod
    def create_key(*args: _Param.args, **kwargs: _Param.kwargs) -> Key:
        return tuple(args), tuple(sorted([*kwargs.items()]))

@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator, _Future](
    decorator.Decorated[_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    decorated_by_instance: weakref.WeakKeyDictionary[
        decorator.Instance, typing.Self,
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
class Decorator[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Decorator[_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): size: int = sys.maxsize


LruCache = Decorator
