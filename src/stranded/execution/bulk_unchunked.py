import dataclasses

from . import decorator
from .abc import bulk_unchunked


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, bulk_unchunked.Decorator): ...


BulkUnchunked = Decorator
