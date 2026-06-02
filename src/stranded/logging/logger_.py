import dataclasses
import typing

from .. import composer_
from .abc import logger_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Logger(composer_.Composer[..., typing.Any], logger_.Logger[..., typing.Any]): ...


Composer = Logger
