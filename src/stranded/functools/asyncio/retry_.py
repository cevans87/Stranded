import dataclasses
import typing

from ..abc import retry_
from ...asyncio import composer_


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], retry_.Composee[ParamT, RetT], typing.Protocol): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], retry_.Connect[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer_.Exit[ParamT, RetT], retry_.Exit[ParamT, RetT]): ...  # type: ignore[misc]


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], retry_.Enter[ParamT, RetT]): ...  # type: ignore[misc]


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], retry_.Composed[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry[**ParamT = ..., RetT = typing.Any](composer_.Composer[ParamT, RetT], retry_.Composer[ParamT, RetT]):
    Composee: typing.ClassVar = Composee
    Connect: typing.ClassVar = Connect
    Exit: typing.ClassVar = Exit
    Enter: typing.ClassVar = Enter
    Composed: typing.ClassVar = Composed


Composer = Retry
retry = Retry()
