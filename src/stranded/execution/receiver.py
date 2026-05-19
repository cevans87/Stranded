import dataclasses

from . import decorator
from .abc import receiver


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, receiver.Decorator): ...


Receiver = Decorator
