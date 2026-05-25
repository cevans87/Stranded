import dataclasses
import typing

from . import decorator
from .abc import when_all_


@dataclasses.dataclass(frozen=True, kw_only=True)
class WhenAll(
    decorator.Decorator[..., typing.Any],
    when_all_.WhenAll[..., typing.Any],
): ...


Decorator = WhenAll
when_all = WhenAll()
