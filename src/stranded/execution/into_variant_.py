import dataclasses

from . import decorator
from .abc import into_variant_


@dataclasses.dataclass(frozen=True, kw_only=True)
class IntoVariant(decorator.Decorator, into_variant_.Decorator): ...


Decorator = IntoVariant
into_variant = IntoVariant()
