import dataclasses

from funktools import decorator
from .abc_ import logger


@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger(decorator.Decorator, logger.Decorator): ...
