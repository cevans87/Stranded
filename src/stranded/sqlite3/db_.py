import dataclasses
import typing

from .. import composer_
from .abc import db_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Db(composer_.Composer[..., typing.Any], db_.Db[..., typing.Any]): ...  # type: ignore[misc]


Composer = Db
db = Db()
