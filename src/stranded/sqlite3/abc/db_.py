from __future__ import annotations

import abc
import ast
import dataclasses
import inspect
import pathlib
import sqlite3
import threading
import typing

from ...abc import composer

type GenerateKey = typing.Callable[..., Key]
type Key = typing.Hashable


Raise = composer.Raise
Stop = composer.Stop
Param = composer.Param
Return = composer.Return


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer.Composee[ParamT, RetT], typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer.Connect[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer.Exit[ParamT, RetT], abc.ABC):
    key: str

    def __call__(self, value: composer.ValueT[ParamT, RetT], /) -> composer.StackT:
        match value:
            case Param() | Raise() | Stop(): pass
            case Return():
                assert self.enter.composer.deserialize(  # type: ignore[attr-defined]
                    ret := self.enter.composer.serialize(value.ret)  # type: ignore[attr-defined]
                ) == value.ret, 'Return value must be deserializable from its serialized form.'

                with self.enter.lock:  # type: ignore[attr-defined]
                    self.enter.connection.execute(  # type: ignore[attr-defined]
                        f'INSERT INTO `{self.enter.table_name}` (key, ret) VALUES (?, ?)',  # type: ignore[attr-defined]
                        (self.key, ret,)
                    )

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer.Enter[ParamT, RetT], abc.ABC):
    # The connection and its per-composition metadata live on the Enter now that
    # Enter/Exit no longer reach Composed.
    connection: sqlite3.Connection
    instance: composer.Instance
    table_name: str
    lock: threading.Lock = dataclasses.field(default_factory=threading.Lock)

    def __call__(self, value: composer.ValueT[ParamT, RetT], /) -> composer.StackT:
        match value:
            case Raise() | Return() | Stop(): return ()
            case Param():
                (bound := inspect.signature(self.composee).bind(*value.args, **value.kwargs)).apply_defaults()
                key = repr((self.instance, bound.args, tuple(sorted(bound.kwargs))))

                with self.lock:
                    ret = self.connection.execute(
                        f'SELECT ret FROM `{self.table_name}` WHERE key = ?',
                        (key,),
                    ).fetchone()
                if ret:
                    return Return(ret=self.composer.deserialize(ret[0])),  # type: ignore[attr-defined]

                return self.exit_t(enter=self, key=key), self.composee,  # type: ignore[call-arg]

        raise ValueError(f'Invalid {value=}')


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer.Composed[ParamT, RetT], abc.ABC):
    def __get__(self, instance: composer.Instance, owner: type[object] | None) -> typing.Self:
        match self.stack[-1]:
            case Enter() as enter_:
                return dataclasses.replace(
                    self,
                    stack=(
                        *self.stack[:-1],
                        dataclasses.replace(
                            enter_, composee=enter_.composee.__get__(instance, owner), instance=instance,
                        ),
                    ),
                )
        assert False, "unreachable"


@dataclasses.dataclass(frozen=True, kw_only=True)
class Db[**ParamT, RetT](composer.Composer[ParamT, RetT], abc.ABC):
    type Version = str

    deserialize: typing.Callable[[str], RetT] = ast.literal_eval
    path: pathlib.Path = pathlib.Path.home() / '.cache' / 'stranded' / 'sqlite3' / 'db'
    serialize: typing.Callable[[RetT], str] = repr
    version: Version = '0.0.0'

    @property
    @abc.abstractmethod
    def composee_t(self) -> type[Composee[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def connect_t(self) -> type[Connect[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def exit_t(self) -> type[Exit[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def enter_t(self) -> type[Enter[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def composed_t(self) -> type[Composed[typing.Any, typing.Any]]: ...

    def __call__(self, composee: Composee[ParamT, RetT], /) -> Composed[ParamT, RetT]:
        table_name = f'{composee.__module__}.{composee.__qualname__}.{self.version}'
        (connection := sqlite3.connect(self.path, check_same_thread=False, isolation_level=None)).execute(
            f'CREATE TABLE IF NOT EXISTS `{table_name}` '  # noqa
            f'(key TEXT PRIMARY KEY NOT NULL UNIQUE, ret TEXT NOT NULL)',  # noqa
        )

        return self.composed_t(  # type: ignore[return-value]
            __doc__=str(composee.__doc__),
            __module__=str(composee.__module__),
            __name__=str(composee.__name__),
            __qualname__=str(composee.__qualname__),
            __signature__=inspect.signature(composee),
            composer=self,
            stack=(
                self.enter_t(  # type: ignore[call-arg]
                    composer=self,
                    composee=composee,
                    connection=connection,
                    instance=None,
                    table_name=table_name,
                ),
            ),
        )


Composer = Db
