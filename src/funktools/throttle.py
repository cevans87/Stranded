import dataclasses

from .abc_ import throttle
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle(decorator.Decorator, throttle.Decorator): ...
