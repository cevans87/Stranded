import dataclasses

from . import decorator
from .abc import transform_sender


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, transform_sender.Decorator): ...


TransformSender = Decorator
