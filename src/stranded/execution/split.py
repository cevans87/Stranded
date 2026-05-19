import dataclasses

from . import decorator
from .abc import split


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, split.Decorator): ...


Split = Decorator
