from __future__ import annotations

import abc
import ast
import collections
import dataclasses
import inspect
import pathlib
import sqlite3
import typing
import weakref

import boltins.decorator.common as decorator


type GenerateKey = typing.Callable[..., Key]
type Key = typing.Hashable

type _Decoratee[** Param, Ret] = Decoratee[Param, Ret]
type _Exit[** Param, Ret] = Exit[Param, Ret]
type _Enter[** Param, Ret] = Enter[Param, Ret]
type _Decorated[** Param, Ret] = Decorated[Param, Ret]
type _Decorator[** Param, Ret] = Decorator[Param, Ret]


class Exception(Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee(decorator.Decoratee, typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[_Enter, _Future](decorator.Exit[_Enter], abc.ABC):
    future: _Future


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[_Decoratee, _Exit, _Decorated, **_Param, _Ret](
    decorator.Enter[_Decoratee, _Exit, _Decorated, _Param],
    abc.ABC,
):
    connection: sqlite3.Connection

    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Ret] | tuple[_Exit, _Decoratee]:
        table_name = f'{self.decorated.__module__}.{self.decorated.__qualname__}'

        (bound := inspect.signature(self.decorated.decoratee).bind(*args, **kwargs)).apply_defaults()
        key = repr((bound.args, tuple(sorted(bound.kwargs))))

        if value := self.connection.execute(f'SELECT value FROM `?` WHERE key = ?', (table_name, key,)).fetchone():
            return ast.literal_eval(value[0]),

        return super().__call__(*args, **kwargs)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[_Decoratee, _Exit, _Enter, _Decorator, _Future](
    decorator.Decorated[_Decoratee, _Exit, _Enter, _Decorator],
    abc.ABC,
): ...

    #connection: sqlite3.Connection = dataclasses.field(default_factory=sqlite3.Connection)
    #instance: decorator.Instance

    #future_by_key: collections.OrderedDict[Key, _Future] = dataclasses.field(default_factory=collections.OrderedDict)

    #def __get__(self, instance, owner) -> typing.Self:
    #    return dataclasses.replace(
    #        self,
    #        decoratee=self.decoratee.__get__(instance, owner),
    #        instance=instance,
    #    )


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[_Decoratee, _Exit, _Enter, _Decorated](
    decorator.Decorator[_Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
):
    path: pathlib.Path | None = None
        #'file::memory:?cache=shared'
        # ':memory:'
