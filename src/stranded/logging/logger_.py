import dataclasses

from .. import decorator
from .abc import logger_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger(decorator.Decorator, logger_.Decorator): ...


Decorator = Logger
