import dataclasses
import typing

from . import decorator
from .abc import stopped_as_error_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StoppedAsError(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    stopped_as_error_.StoppedAsError[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = StoppedAsError
stopped_as_error = StoppedAsError()
