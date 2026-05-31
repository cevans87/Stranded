import dataclasses
import typing

from ...asyncio import composer
from ..abc import db_


@typing.runtime_checkable
class Composee[**ParamT, RetT](
    composer.Composee[ParamT, RetT],
    db_.Composee[ParamT, RetT],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](  # type: ignore[misc]
    composer.Exit[ParamT, RetT],
    db_.Exit[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](  # type: ignore[misc]
    composer.Enter[ParamT, RetT],
    db_.Enter[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](
    composer.Composed[ParamT, RetT],
    db_.Composed[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Db[**ParamT, RetT](
    composer.Composer[ParamT, RetT],
    db_.Composer[ParamT, RetT],
):
    composee_t: typing.ClassVar = Composee
    exit_t: typing.ClassVar = Exit  # type: ignore[assignment]
    enter_t: typing.ClassVar = Enter
    composed_t: typing.ClassVar = Composed
Composer = Db
db: Db[..., typing.Any] = Db()
