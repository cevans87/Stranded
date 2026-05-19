import dataclasses

from . import decorator
from .abc import sender


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, sender.Decorator): ...


Sender = Decorator
