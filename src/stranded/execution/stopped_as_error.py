import dataclasses

from . import decorator
from .abc import stopped_as_error


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, stopped_as_error.Decorator): ...


StoppedAsError = Decorator
