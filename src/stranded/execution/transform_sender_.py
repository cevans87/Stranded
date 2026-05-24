import dataclasses
import typing

from . import decorator
from .abc import transform_sender_


@dataclasses.dataclass(frozen=True, kw_only=True)
class TransformSender(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    transform_sender_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = TransformSender
transform_sender = TransformSender()
