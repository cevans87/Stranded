import dataclasses
import typing

from . import decorator
from .abc import stop_source_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StopSource(
    decorator.Decorator[..., typing.Any],
    stop_source_.StopSource[..., typing.Any],
): ...


Decorator = StopSource
stop_source = StopSource()
