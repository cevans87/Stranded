import dataclasses
import typing

from . import decorator
from .abc import let_value_


@dataclasses.dataclass(frozen=True, kw_only=True)
class LetValue(
    decorator.Decorator[..., typing.Any],
    let_value_.LetValue[..., typing.Any],
): ...


Decorator = LetValue
let_value = LetValue()
