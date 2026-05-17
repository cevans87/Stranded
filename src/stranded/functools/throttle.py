import dataclasses

from .abc import throttle
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, throttle.Decorator): ...


Throttle = Decorator
