import dataclasses

from . import decorator
from .abc import let_error


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, let_error.Decorator): ...


LetError = Decorator
