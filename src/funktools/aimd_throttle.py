import dataclasses

from .abc_ import aimd_throttle as abc_aimd_throttle
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class AimdThrottle(decorator.Decorator, abc_aimd_throttle.Decorator): ...
