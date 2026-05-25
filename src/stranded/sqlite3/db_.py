import dataclasses
import typing

from .. import decorator
from .abc import db_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Db(  # type: ignore[misc]
    decorator.Decorator[..., typing.Any],
    db_.Db[..., typing.Any],
): ...


Decorator = Db
db = Db()
