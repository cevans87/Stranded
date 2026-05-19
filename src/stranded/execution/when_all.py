import dataclasses

from . import decorator
from .abc import when_all


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, when_all.Decorator): ...


WhenAll = Decorator
