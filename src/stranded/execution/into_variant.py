import dataclasses

from . import decorator
from .abc import into_variant


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, into_variant.Decorator): ...


IntoVariant = Decorator
