import dataclasses

from . import decorator
from .abc import just_stopped


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, just_stopped.Decorator): ...


JustStopped = Decorator
