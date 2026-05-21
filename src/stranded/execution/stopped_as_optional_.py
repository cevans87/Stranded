import dataclasses

from . import decorator
from .abc import stopped_as_optional_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StoppedAsOptional(decorator.Decorator, stopped_as_optional_.Decorator): ...


Decorator = StoppedAsOptional
stopped_as_optional = StoppedAsOptional()
