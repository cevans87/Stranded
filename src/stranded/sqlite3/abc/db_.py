from __future__ import annotations

import abc
import ast
import dataclasses
import inspect
import pathlib
import sqlite3
import threading
import typing

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
    key: str

    @abc.abstractmethod
    def __call__(self, result: decorator.Raise | RetT) -> ():
        if not isinstance(result, decorator.Raise):
            assert self.enter.decorated.decorator.deserialize(
                value := self.enter.decorated.decorator.serialize(result)
            ) == result, 'Return value must be deserializable from its serialized form.'

            with self.enter.decorated.lock:
                self.enter.decorated.connection.execute(
                    f'INSERT INTO `{self.enter.decorated.table_name}` (key, value) VALUES (?, ?)',  # noqa
                    (self.key, value,)
                )

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[** ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Enter[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    @abc.abstractmethod
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> tuple[RetT] | tuple[ExitT, DecorateeT]:
        (bound := inspect.signature(self.decorated.decoratee).bind(*args, **kwargs)).apply_defaults()
        key = repr((self.decorated.instance, bound.args, tuple(sorted(bound.kwargs))))

        with self.decorated.lock:
            value = self.decorated.connection.execute(
                f'SELECT value FROM `{self.decorated.table_name}` WHERE key = ?',  # noqa
                (key,),
            ).fetchone()
        if value:
            return self.decorated.decorator.serialize(value[0])

        return self.exit_t(enter=self, key=key), self.decorated.decoratee,


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorated[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    connection: sqlite3.Connection
    instance: decorator.Instance
    table_name: str
    lock: threading.Lock = dataclasses.field(default_factory=threading.Lock)

    def __get__(self, instance: decorator.Instance, owner) -> typing.Self:
        return dataclasses.replace(self, decoratee=self.decoratee.__get__(instance, owner), instance=instance)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Db[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorator[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    type Version = str

    deserialize: typing.Callable[[str], RetT] = ast.literal_eval
    path: pathlib.Path = pathlib.Path.home() / '.cache' / 'stranded' / 'sqlite3' / 'db'
    serialize: typing.Callable[[RetT], str] = repr
    version: Version = '0.0.0'

    def __call__(self, decoratee: DecorateeT, /) -> DecoratedT:
        table_name = f'{decoratee.__module__}.{decoratee.__qualname__}.{self.version}'
        (connection := sqlite3.connect(self.path, check_same_thread=False, isolation_level=None)).execute(
            f'CREATE TABLE IF NOT EXISTS `{table_name}` '  # noqa
            f'(key STRING PRIMARY KEY NOT NULL UNIQUE, value STRING NOT NULL)',  # noqa
        )

        return self.decorated_t(
            __doc__=str(decoratee.__doc__),
            __module__=str(decoratee.__module__),
            __name__=str(decoratee.__name__),
            __qualname__=str(decoratee.__qualname__),
            __signature__=inspect.signature(decoratee),
            connection=connection,
            decoratee=decoratee,
            decorator=self,
            instance=None,
            table_name=table_name,
        )


Decorator = Db
db = Db()
