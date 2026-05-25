import dataclasses
import typing

from .. import decorator
from .abc import logger_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger(
    decorator.Decorator[..., typing.Any],
    logger_.Logger[..., typing.Any],
): ...


Decorator = Logger
