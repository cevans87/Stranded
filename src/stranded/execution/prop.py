import dataclasses

from . import decorator
from .abc import prop


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, prop.Decorator): ...


Prop = Decorator
