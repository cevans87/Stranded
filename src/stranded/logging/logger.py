import dataclasses

from .. import decorator
from .abc import logger


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, logger.Decorator): ...


Logger = Decorator
