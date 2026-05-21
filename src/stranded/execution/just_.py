import dataclasses

from . import decorator
from .abc import just_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Just(decorator.Decorator, just_.Decorator): ...


Decorator = Just
just = Just()
