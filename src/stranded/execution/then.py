import dataclasses

from . import decorator
from .abc import then


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, then.Decorator): ...


Then = Decorator
