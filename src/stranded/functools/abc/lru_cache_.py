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
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT, FutureT](
    decorator.Send[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT, FutureT](
    decorator.Receive[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT, FutureT](
    decorator.Exit[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): key: Key


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Enter[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    @staticmethod
    def create_key(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Key:
        return tuple(args), tuple(sorted([*kwargs.items()]))

@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT, FutureT](
    decorator.Decorated[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    decorated_by_instance: weakref.WeakKeyDictionary[
        decorator.Instance, typing.Self,
    ] = dataclasses.field(default_factory=weakref.WeakKeyDictionary)
    future_by_key: collections.OrderedDict[Key, FutureT] = dataclasses.field(default_factory=collections.OrderedDict)

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
class LruCache[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorator[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): size: int = sys.maxsize


Decorator = LruCache
# TODO(claude): This instantiates from an abstract class. We shouldn't do this pattern with any of the abstract base
#  decorators. Note that we also export this in this directory's __init__.py file, so that export will need to go away.
lru_cache = LruCache()
