import dataclasses
import typing

from . import decorator
from .abc import bulk_unchunked_


@dataclasses.dataclass(frozen=True, kw_only=True)
class BulkUnchunked(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    bulk_unchunked_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = BulkUnchunked
bulk_unchunked = BulkUnchunked()
