import dataclasses
import typing

from . import decorator
from .abc import bulk_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Bulk(
    decorator.Decorator[..., typing.Any],
    bulk_.Bulk[..., typing.Any],
): ...


Decorator = Bulk
bulk = Bulk()
