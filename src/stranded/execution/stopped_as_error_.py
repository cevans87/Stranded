import dataclasses

from . import decorator
from .abc import stopped_as_error_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StoppedAsError(decorator.Decorator, stopped_as_error_.Decorator): ...


Decorator = StoppedAsError
stopped_as_error = StoppedAsError()
