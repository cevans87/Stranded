import dataclasses

from . import decorator
from .abc import just_error


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, just_error.Decorator): ...


JustError = Decorator
