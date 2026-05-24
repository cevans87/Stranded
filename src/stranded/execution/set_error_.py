import dataclasses
import typing

from . import decorator
from .abc import set_error_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SetError(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    set_error_.SetError[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = SetError
set_error = SetError()
