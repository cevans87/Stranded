import dataclasses
import typing

from ...threading import decorator
from ..abc import db_


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    db_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](  # type: ignore[misc]
    decorator.Exit[ParamT, RetT],
    db_.Exit[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](  # type: ignore[misc]
    decorator.Enter[ParamT, RetT],
    db_.Enter[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    db_.Decorated[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Db[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    db_.Decorator[ParamT, RetT],
):
    decoratee_t: typing.ClassVar = Decoratee
    exit_t: typing.ClassVar = Exit  # type: ignore[assignment]
    enter_t: typing.ClassVar = Enter
    decorated_t: typing.ClassVar = Decorated  # type: ignore[assignment]
Decorator = Db
db: Db[..., typing.Any] = Db()
