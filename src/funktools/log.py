import dataclasses

from .abc_ import log
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Log(decorator.Decorator, log.Decorator): ...
