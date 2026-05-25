import dataclasses
import typing

from . import decorator
from .abc import inplace_stop_source_


@dataclasses.dataclass(frozen=True, kw_only=True)
class InplaceStopSource(
    decorator.Decorator[..., typing.Any],
    inplace_stop_source_.InplaceStopSource[..., typing.Any],
): ...


Decorator = InplaceStopSource
inplace_stop_source = InplaceStopSource()
