import dataclasses

from . import decorator
from .abc import bulk


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, bulk.Decorator): ...


Bulk = Decorator
