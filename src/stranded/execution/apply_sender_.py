import dataclasses
import typing

from . import decorator
from .abc import apply_sender_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ApplySender(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    apply_sender_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = ApplySender
apply_sender = ApplySender()
