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


Raise = decorator.Raise
Stop = decorator.Stop
Param = decorator.Param
Return = decorator.Return


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    abc.ABC,
):
    key: str

    def __call__(self, value: decorator.ValueT[ParamT, RetT], /) -> decorator.StackT:
        match value:
            case Param() | Raise() | Stop(): pass
            case Return():
                assert self.enter.decorator.deserialize(  # type: ignore[attr-defined]
                    ret := self.enter.decorator.serialize(value.ret)  # type: ignore[attr-defined]
                ) == value.ret, 'Return value must be deserializable from its serialized form.'

                with self.enter.lock:  # type: ignore[attr-defined]
                    self.enter.connection.execute(  # type: ignore[attr-defined]
                        f'INSERT INTO `{self.enter.table_name}` (key, ret) VALUES (?, ?)',  # type: ignore[attr-defined]
                        (self.key, ret,)
                    )

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    abc.ABC,
):
    # The connection and its per-decoration metadata live on the Enter now that
    # Enter/Exit no longer reach Decorated.
    connection: sqlite3.Connection
    instance: decorator.Instance
    table_name: str
    lock: threading.Lock = dataclasses.field(default_factory=threading.Lock)

    def __call__(self, value: decorator.ValueT[ParamT, RetT], /) -> decorator.StackT:
        match value:
            case Raise() | Return() | Stop(): return ()
            case Param():
                (bound := inspect.signature(self.decoratee).bind(*value.args, **value.kwargs)).apply_defaults()
                key = repr((self.instance, bound.args, tuple(sorted(bound.kwargs))))

                with self.lock:
                    ret = self.connection.execute(
                        f'SELECT ret FROM `{self.table_name}` WHERE key = ?',
                        (key,),
                    ).fetchone()
                if ret:
                    return Return(ret=self.decorator.serialize(ret[0])),  # type: ignore[attr-defined]

                return self.exit_t(enter=self, key=key), self.decoratee,  # type: ignore[call-arg, return-value]

        raise ValueError(f'Invalid {value=}')


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    abc.ABC,
):
    def __get__(self, instance: decorator.Instance, owner: type[object] | None) -> typing.Self:
        match self.stack:
            case [*rest, Enter() as enter_]:
                return dataclasses.replace(
                    self,
                    stack=(
                        *rest,
                        dataclasses.replace(
                            enter_, decoratee=enter_.decoratee.__get__(instance, owner), instance=instance,
                        ),
                    ),
                )
        assert False, "unreachable"


@dataclasses.dataclass(frozen=True, kw_only=True)
class Db[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    abc.ABC,
):
    type Version = str

    deserialize: typing.Callable[[str], RetT] = ast.literal_eval
    path: pathlib.Path = pathlib.Path.home() / '.cache' / 'stranded' / 'sqlite3' / 'db'
    serialize: typing.Callable[[RetT], str] = repr
    version: Version = '0.0.0'

    def __call__(self, decoratee: Decoratee[ParamT, RetT], /) -> Decorated[ParamT, RetT]:
        table_name = f'{decoratee.__module__}.{decoratee.__qualname__}.{self.version}'  # type: ignore[attr-defined]
        (connection := sqlite3.connect(self.path, check_same_thread=False, isolation_level=None)).execute(
            f'CREATE TABLE IF NOT EXISTS `{table_name}` '  # noqa
            f'(key STRING PRIMARY KEY NOT NULL UNIQUE, ret STRING NOT NULL)',  # noqa
        )

        return self.decorated_t(  # type: ignore[return-value]
            __doc__=str(decoratee.__doc__),
            __module__=str(decoratee.__module__),
            __name__=str(decoratee.__name__),  # type: ignore[attr-defined]
            __qualname__=str(decoratee.__qualname__),  # type: ignore[attr-defined]
            __signature__=inspect.signature(decoratee),
            decorator=self,
            stack=(
                self.enter_t(  # type: ignore[call-arg]
                    decorator=self,
                    decoratee=decoratee,
                    connection=connection,
                    instance=None,
                    table_name=table_name,
                ),
            ),
        )


Decorator = Db
