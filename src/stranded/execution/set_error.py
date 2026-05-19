import dataclasses

from . import decorator
from .abc import set_error


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, set_error.Decorator): ...


SetError = Decorator
