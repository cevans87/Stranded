import dataclasses

from .. import decorator
from .abc import db_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Db(decorator.Decorator, db_.Decorator): ...


Decorator = Db
db = Db()
