import dataclasses
import typing

from . import decorator
from .abc import let_error_


@dataclasses.dataclass(frozen=True, kw_only=True)
class LetError(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    let_error_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = LetError
let_error = LetError()
