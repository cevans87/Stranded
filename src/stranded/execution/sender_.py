import dataclasses
import typing

from . import decorator
from .abc import sender_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Sender(
    decorator.Decorator[..., typing.Any],
    sender_.Sender[..., typing.Any],
): ...


Decorator = Sender
sender = Sender()
