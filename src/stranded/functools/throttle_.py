import dataclasses

from .abc import throttle_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle(decorator.Decorator, throttle_.Decorator): ...


Decorator = Throttle
throttle = Throttle()
