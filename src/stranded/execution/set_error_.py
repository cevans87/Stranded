import dataclasses

from . import decorator
from .abc import set_error_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SetError(decorator.Decorator, set_error_.Decorator): ...


Decorator = SetError
set_error = SetError()
