import dataclasses

from . import decorator
from .abc import bulk_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Bulk(decorator.Decorator, bulk_.Decorator): ...


Decorator = Bulk
bulk = Bulk()
