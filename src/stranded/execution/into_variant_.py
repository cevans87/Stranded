import dataclasses
import typing

from . import decorator
from .abc import into_variant_


@dataclasses.dataclass(frozen=True, kw_only=True)
class IntoVariant(
    decorator.Decorator[..., typing.Any],
    into_variant_.IntoVariant[..., typing.Any],
): ...


Decorator = IntoVariant
into_variant = IntoVariant()
