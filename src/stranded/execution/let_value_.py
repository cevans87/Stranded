import dataclasses

from . import decorator
from .abc import let_value_


@dataclasses.dataclass(frozen=True, kw_only=True)
class LetValue(decorator.Decorator, let_value_.Decorator): ...


Decorator = LetValue
let_value = LetValue()
