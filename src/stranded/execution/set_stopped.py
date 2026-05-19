import dataclasses

from . import decorator
from .abc import set_stopped


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, set_stopped.Decorator): ...


SetStopped = Decorator
