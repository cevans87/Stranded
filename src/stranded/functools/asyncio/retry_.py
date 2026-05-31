import dataclasses
import typing

from ..abc import retry_
from ...asyncio import composer


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer.Composee[ParamT, RetT], retry_.Composee[ParamT, RetT], typing.Protocol): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer.Connect[ParamT, RetT], retry_.Connect[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer.Exit[ParamT, RetT], retry_.Exit[ParamT, RetT]): ...  # type: ignore[misc]


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer.Enter[ParamT, RetT], retry_.Enter[ParamT, RetT]): ...  # type: ignore[misc]


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer.Composed[ParamT, RetT], retry_.Composed[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry[**ParamT, RetT](composer.Composer[ParamT, RetT], retry_.Composer[ParamT, RetT]):
    composee_t: typing.ClassVar = Composee
    connect_t: typing.ClassVar = Connect
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    composed_t: typing.ClassVar = Composed
Composer = Retry
retry: Retry[..., typing.Any] = Retry()
