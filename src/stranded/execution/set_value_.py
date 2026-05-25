import dataclasses
import typing

from . import decorator
from .abc import set_value_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SetValue(
    decorator.Decorator[..., typing.Any],
    set_value_.SetValue[..., typing.Any],
): ...


Decorator = SetValue
set_value = SetValue()
