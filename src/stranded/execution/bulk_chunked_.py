import dataclasses
import typing

from . import decorator
from .abc import bulk_chunked_


@dataclasses.dataclass(frozen=True, kw_only=True)
class BulkChunked(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    bulk_chunked_.BulkChunked[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = BulkChunked
bulk_chunked = BulkChunked()
