import dataclasses

from . import decorator
from .abc import ensure_started_


@dataclasses.dataclass(frozen=True, kw_only=True)
class EnsureStarted(decorator.Decorator, ensure_started_.Decorator): ...


Decorator = EnsureStarted
ensure_started = EnsureStarted()
