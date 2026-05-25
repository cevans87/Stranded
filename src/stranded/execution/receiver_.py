import dataclasses
import typing

from . import decorator
from .abc import receiver_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receiver(
    decorator.Decorator[..., typing.Any],
    receiver_.Receiver[..., typing.Any],
): ...


Decorator = Receiver
receiver = Receiver()
