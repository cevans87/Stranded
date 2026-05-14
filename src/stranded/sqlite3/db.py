import dataclasses

from .. import decorator
from .abc import db


@dataclasses.dataclass(frozen=True, kw_only=True)
class Db(decorator.Decorator, db.Decorator): ...
