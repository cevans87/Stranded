import dataclasses

from . import decorator
from .abc import bulk_chunked_


@dataclasses.dataclass(frozen=True, kw_only=True)
class BulkChunked(decorator.Decorator, bulk_chunked_.Decorator): ...


Decorator = BulkChunked
bulk_chunked = BulkChunked()
