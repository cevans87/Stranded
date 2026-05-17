import dataclasses

from . import decorator
from .abc import upon_error


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, upon_error.Decorator): ...


UponError = Decorator
