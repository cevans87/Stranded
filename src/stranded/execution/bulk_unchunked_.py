import dataclasses

from . import decorator
from .abc import bulk_unchunked_


@dataclasses.dataclass(frozen=True, kw_only=True)
class BulkUnchunked(decorator.Decorator, bulk_unchunked_.Decorator): ...


Decorator = BulkUnchunked
bulk_unchunked = BulkUnchunked()
