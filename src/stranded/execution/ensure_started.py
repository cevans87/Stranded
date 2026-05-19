import dataclasses

from . import decorator
from .abc import ensure_started


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, ensure_started.Decorator): ...


EnsureStarted = Decorator
