import dataclasses
import typing

from .. import composer
from .abc import logger_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger(composer.Composer[..., typing.Any], logger_.Logger[..., typing.Any]): ...


Composer = Logger
