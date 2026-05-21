import dataclasses

from . import decorator
from .abc import upon_error_


@dataclasses.dataclass(frozen=True, kw_only=True)
class UponError(decorator.Decorator, upon_error_.Decorator): ...


Decorator = UponError
upon_error = UponError()
