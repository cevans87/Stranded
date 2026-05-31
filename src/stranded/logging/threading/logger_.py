import dataclasses
import typing

from ...threading import composer
from ..abc import logger_

@typing.runtime_checkable
class Composee[**ParamT, RetT](
    composer.Composee[ParamT, RetT],
    logger_.Composee[ParamT, RetT],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    composer.Exit[ParamT, RetT],
    logger_.Exit[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    composer.Enter[ParamT, RetT],
    logger_.Enter[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](
    composer.Composed[ParamT, RetT],
    logger_.Composed[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger[**ParamT, RetT](
    composer.Composer[ParamT, RetT],
    logger_.Composer[ParamT, RetT],
):
    composee_t: typing.ClassVar = Composee
    exit_t: typing.ClassVar = Exit  # type: ignore[assignment]
    enter_t: typing.ClassVar = Enter
    composed_t: typing.ClassVar = Composed
Composer = Logger
