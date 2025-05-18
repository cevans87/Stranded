import dataclasses

from ..funktools import decorator
from .abc_ import db


@dataclasses.dataclass(frozen=True, kw_only=True)
class Db(decorator.Decorator, db.Decorator): ...
