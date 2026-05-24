import dataclasses
import typing

from . import decorator
from .abc import bulk_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Bulk(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    bulk_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = Bulk
bulk = Bulk()
