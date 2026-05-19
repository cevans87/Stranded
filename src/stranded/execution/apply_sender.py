import dataclasses

from . import decorator
from .abc import apply_sender


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, apply_sender.Decorator): ...


ApplySender = Decorator
