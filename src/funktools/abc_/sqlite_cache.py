from __future__ import annotations

import abc
import ast
import dataclasses
import inspect
import pathlib
import sqlite3
import textwrap
import typing

from . import decorator


type GenerateKey = typing.Callable[..., Key]
type Key = typing.Hashable

class Exception(decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee(decorator.Decoratee, typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[_Enter, _Ret](decorator.Exit[_Enter, _Ret], abc.ABC):
    key: str

    def __call__(self, result: decorator.Raise | _Ret) -> ():
        if not isinstance(result, decorator.Raise):
            self.enter.connection.execute(
                'INSERT INTO `?` (key, value) VALUES (`?`, `?`)'
                (self.enter.decorator.table_name, self.key, repr(result))
            )

        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[_Decoratee, _Exit, _Decorated, **_Param, _Ret](
    decorator.Enter[_Decoratee, _Exit, _Decorated, _Param],
    abc.ABC,
):
    connection: sqlite3.Connection

    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Ret] | tuple[_Exit, _Decoratee]:
        (bound := inspect.signature(self.decorated.decoratee).bind(*args, **kwargs)).apply_defaults()
        key = repr((bound.args, tuple(sorted(bound.kwargs))))

        if value := self.connection.execute(
            'SELECT value FROM `?` WHERE key = `?`',
            (self.decorated.table_name, key,),
        ).fetchone():
            return ast.literal_eval(value[0]),

        return super().__call__(*args, **kwargs)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[_Decoratee, _Exit, _Enter, _Decorator, _Future](
    decorator.Decorated[_Decoratee, _Exit, _Enter, _Decorator],
    abc.ABC,
):
    def __get__(self, instance: decorator.Instance, owner) -> typing.Self:
        # TODO make sure instance is reproducible somehow across process invocations.
        assert instance.__repr__ is not object.__repr__
        return

    def __post_init__(self) -> None:
        self.connection.execute(

            textwrap.dedent(f'''
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                key STRING PRIMARY KEY NOT NULL UNIQUE,
                value STRING NOT NULL
            )
        ''').strip())

    @property
    def table_name(self) -> str:
        return f'{self.__module__}.{self.__qualname__}.{self.instance!r}'


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[_Decoratee, _Exit, _Enter, _Decorated](
    decorator.Decorator[_Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
):
    path: pathlib.Path = pathlib.Path.home() / '.cache' / 'stranded' / 'sqlite_cache'
