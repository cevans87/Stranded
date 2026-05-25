import dataclasses
import typing

from . import decorator
from .abc import set_error_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SetError(
    decorator.Decorator[..., typing.Any],
    set_error_.SetError[..., typing.Any],
): ...


Decorator = SetError
set_error = SetError()
