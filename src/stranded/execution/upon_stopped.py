import dataclasses

from . import decorator
from .abc import upon_stopped


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, upon_stopped.Decorator): ...


UponStopped = Decorator
