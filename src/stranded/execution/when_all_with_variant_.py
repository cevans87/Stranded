import dataclasses

from . import decorator
from .abc import when_all_with_variant_


@dataclasses.dataclass(frozen=True, kw_only=True)
class WhenAllWithVariant(decorator.Decorator, when_all_with_variant_.Decorator): ...


Decorator = WhenAllWithVariant
when_all_with_variant = WhenAllWithVariant()
