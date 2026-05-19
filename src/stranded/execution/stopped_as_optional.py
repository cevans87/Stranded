import dataclasses

from . import decorator
from .abc import stopped_as_optional


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, stopped_as_optional.Decorator): ...


StoppedAsOptional = Decorator
