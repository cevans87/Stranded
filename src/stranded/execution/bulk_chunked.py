import dataclasses

from . import decorator
from .abc import bulk_chunked


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, bulk_chunked.Decorator): ...


BulkChunked = Decorator
