import dataclasses

from funktools import decorator
from .abc_ import logger as abc_logger


@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger(decorator.Decorator, abc_logger.Decorator): ...
