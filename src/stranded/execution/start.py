import dataclasses

from . import decorator
from .abc import start


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, start.Decorator): ...


Start = Decorator
