import dataclasses

from . import decorator
from .abc import set_value_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SetValue(decorator.Decorator, set_value_.Decorator): ...


Decorator = SetValue
set_value = SetValue()
