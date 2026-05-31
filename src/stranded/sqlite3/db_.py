import dataclasses
import typing

from .. import composer
from .abc import db_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Db(  # type: ignore[misc]
    composer.Composer[..., typing.Any],
    db_.Db[..., typing.Any],
): ...


Composer = Db
db = Db()
