from __future__ import annotations

import abc
import collections
import dataclasses
import typing
import weakref
import sys

from . import decorator


type GenerateKey = typing.Callable[..., Key]
type Key = typing.Hashable


class Exception(decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee(decorator.Decoratee, typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[_Enter, _Ret, _Future](decorator.Exit[_Enter, _Ret], abc.ABC):
    future: _Future


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[_Decoratee, _Exit, _Decorated, **_Param](
    decorator.Enter[_Decoratee, _Exit, _Decorated, _Param],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[_Decoratee, _Exit, _Enter, _Decorator, _Future](
    decorator.Decorated[_Decoratee, _Exit, _Enter, _Decorator],
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
class Decorator[_Decoratee, _Exit, _Enter, _Decorated](
    decorator.Decorator[_Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
):
    generate_key: GenerateKey = lambda *args, **kwargs: (tuple(args), tuple(sorted([*kwargs.items()])))
    size: int = sys.maxsize
