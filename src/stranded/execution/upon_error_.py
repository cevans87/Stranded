import dataclasses
import typing

from . import decorator
from .abc import upon_error_


@dataclasses.dataclass(frozen=True, kw_only=True)
class UponError(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    upon_error_.UponError[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = UponError
upon_error = UponError()
