import dataclasses

from . import decorator
from .abc import when_all_with_variant


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, when_all_with_variant.Decorator): ...


WhenAllWithVariant = Decorator
