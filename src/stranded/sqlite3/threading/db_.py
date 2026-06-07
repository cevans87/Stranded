import dataclasses
import typing

from ...threading import composer_
from ..abc import db_


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], db_.Composee[ParamT, RetT], typing.Protocol): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], db_.Connect[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer_.Exit[ParamT, RetT], db_.Exit[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], db_.Enter[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], db_.Composed[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Db[**ParamT = ..., RetT = typing.Any](composer_.Composer[ParamT, RetT], db_.Composer[ParamT, RetT]):
    Composee: typing.ClassVar = Composee
    Connect: typing.ClassVar = Connect
    Exit: typing.ClassVar = Exit
    Enter: typing.ClassVar = Enter
    Composed: typing.ClassVar = Composed


Composer = Db
db = Db()
