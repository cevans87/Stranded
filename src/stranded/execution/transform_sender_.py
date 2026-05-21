import dataclasses

from . import decorator
from .abc import transform_sender_


@dataclasses.dataclass(frozen=True, kw_only=True)
class TransformSender(decorator.Decorator, transform_sender_.Decorator): ...


Decorator = TransformSender
transform_sender = TransformSender()
