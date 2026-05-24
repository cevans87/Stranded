import dataclasses
import typing

from . import decorator
from .abc import let_value_


@dataclasses.dataclass(frozen=True, kw_only=True)
class LetValue(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    let_value_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = LetValue
let_value = LetValue()
