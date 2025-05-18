from __future__ import annotations

import abc
import ast
import dataclasses
import inspect
import pathlib
import sqlite3
import threading
import typing

from ...funktools.abc_ import decorator

type GenerateKey = typing.Callable[..., Key]
type Key = typing.Hashable


class Exception(decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**_Param, _Ret, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Decoratee[_Param, _Ret, _Exit, _Enter, _Decorated, _Decorator],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator](
    decorator.Exit[_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    key: str

    @abc.abstractmethod
    def __call__(self, result: decorator.Raise | _Ret) -> ():
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
class Enter[** _Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator](
    decorator.Enter[_Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator],
    abc.ABC,
):
    @abc.abstractmethod
    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Ret] | tuple[_Exit, _Decoratee]:
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
class Decorated[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator](
    decorator.Decorated[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator],
    abc.ABC,
):
    connection: sqlite3.Connection
    instance: decorator.Instance
    table_name: str
    lock: threading.Lock = dataclasses.field(default_factory=threading.Lock)

    def __get__(self, instance: decorator.Instance, owner) -> typing.Self:
        return dataclasses.replace(self, decoratee=self.decoratee.__get__(instance, owner), instance=instance)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated](
    decorator.Decorator[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
):
    type Version = tuple[int, int, int]

    deserialize: typing.Callable[[str], _Ret] = ast.literal_eval
    path: pathlib.Path = pathlib.Path.home() / '.cache' / 'stranded' / 'sqlittle' / 'cache'
    serialize: typing.Callable[[_Ret], str] = repr
    version: Version = (0, 0, 0)

    def __call__(self, decoratee: _Decoratee, /) -> _Decorated:
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
