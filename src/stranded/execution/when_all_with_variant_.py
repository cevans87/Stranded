import dataclasses
import typing

from . import decorator
from .abc import when_all_with_variant_


@dataclasses.dataclass(frozen=True, kw_only=True)
class WhenAllWithVariant(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    when_all_with_variant_.WhenAllWithVariant[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = WhenAllWithVariant
when_all_with_variant = WhenAllWithVariant()
