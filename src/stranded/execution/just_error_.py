import dataclasses

from . import decorator
from .abc import just_error_


@dataclasses.dataclass(frozen=True, kw_only=True)
class JustError(decorator.Decorator, just_error_.Decorator): ...


Decorator = JustError
just_error = JustError()
