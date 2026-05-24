import dataclasses
import typing

from . import decorator
from .abc import just_error_


@dataclasses.dataclass(frozen=True, kw_only=True)
class JustError(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    just_error_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = JustError
just_error = JustError()
