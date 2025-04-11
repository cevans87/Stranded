import dataclasses

from .abc_ import throttle as abc_throttle
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle(decorator.Decorator, abc_throttle.Decorator): ...
