import dataclasses

from . import decorator
from .abc import let_error_


@dataclasses.dataclass(frozen=True, kw_only=True)
class LetError(decorator.Decorator, let_error_.Decorator): ...


Decorator = LetError
let_error = LetError()
