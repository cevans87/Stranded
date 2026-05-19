import dataclasses

from . import decorator
from .abc import starts_on


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, starts_on.Decorator): ...


StartsOn = Decorator
