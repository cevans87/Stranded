import dataclasses
import typing

from ...asyncio import decorator
from ..abc import logger_

@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    logger_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](  # type: ignore[misc]
    decorator.Exit[ParamT, RetT],
    logger_.Exit[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](  # type: ignore[misc]
    decorator.Enter[ParamT, RetT],
    logger_.Enter[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    logger_.Decorated[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    logger_.Decorator[ParamT, RetT],
):
    decoratee_t: typing.ClassVar = Decoratee
    exit_t: typing.ClassVar = Exit  # type: ignore[assignment]
    enter_t: typing.ClassVar = Enter
    decorated_t: typing.ClassVar = Decorated
Decorator = Logger
