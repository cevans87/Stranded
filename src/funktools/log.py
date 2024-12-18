import dataclasses

from .abc_ import log as abc_log
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Log(decorator.Decorator, abc_log.Decorator): ...
