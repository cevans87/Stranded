import dataclasses

from . import decorator
from .abc import let_stopped


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, let_stopped.Decorator): ...


LetStopped = Decorator
