import dataclasses

from . import decorator
from .abc import stop_source_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StopSource(decorator.Decorator, stop_source_.Decorator): ...


Decorator = StopSource
stop_source = StopSource()
