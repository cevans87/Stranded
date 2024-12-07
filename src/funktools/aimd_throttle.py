import dataclasses

from .abc_ import aimd_throttle
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class AimdThrottle(decorator.Decorator, aimd_throttle.Decorator): ...
