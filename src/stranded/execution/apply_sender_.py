import dataclasses
import typing

from . import decorator
from .abc import apply_sender_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ApplySender(
    decorator.Decorator[..., typing.Any],
    apply_sender_.ApplySender[..., typing.Any],
): ...


Decorator = ApplySender
apply_sender = ApplySender()
