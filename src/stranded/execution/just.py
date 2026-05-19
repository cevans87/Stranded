import dataclasses

from . import decorator
from .abc import just


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, just.Decorator): ...


Just = Decorator
