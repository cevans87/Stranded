import dataclasses

from . import decorator
from .abc import apply_sender_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ApplySender(decorator.Decorator, apply_sender_.Decorator): ...


Decorator = ApplySender
apply_sender = ApplySender()
