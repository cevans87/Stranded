import dataclasses
import typing

from ...threading import composer_
from ..abc import logger_

@typing.runtime_checkable
class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], logger_.Composee[ParamT, RetT], typing.Protocol): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], logger_.Connect[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer_.Exit[ParamT, RetT], logger_.Exit[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], logger_.Enter[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], logger_.Composed[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger[**ParamT, RetT](composer_.Composer[ParamT, RetT], logger_.Composer[ParamT, RetT]):
    Composee: typing.ClassVar = Composee
    Connect: typing.ClassVar = Connect
    Exit: typing.ClassVar = Exit  # type: ignore[assignment]
    Enter: typing.ClassVar = Enter
    Composed: typing.ClassVar = Composed


Composer = Logger
