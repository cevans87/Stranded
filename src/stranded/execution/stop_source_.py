import dataclasses
import typing

from . import decorator
from .abc import stop_source_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StopSource(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    stop_source_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = StopSource
stop_source = StopSource()
