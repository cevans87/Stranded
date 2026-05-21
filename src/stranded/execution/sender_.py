import dataclasses

from . import decorator
from .abc import sender_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Sender(decorator.Decorator, sender_.Decorator): ...


Decorator = Sender
sender = Sender()
