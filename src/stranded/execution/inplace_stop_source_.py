import dataclasses

from . import decorator
from .abc import inplace_stop_source_


@dataclasses.dataclass(frozen=True, kw_only=True)
class InplaceStopSource(decorator.Decorator, inplace_stop_source_.Decorator): ...


Decorator = InplaceStopSource
inplace_stop_source = InplaceStopSource()
