import dataclasses

from . import decorator
from .abc import receiver_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receiver(decorator.Decorator, receiver_.Decorator): ...


Decorator = Receiver
receiver = Receiver()
