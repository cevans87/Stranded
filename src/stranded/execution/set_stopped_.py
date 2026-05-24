import dataclasses
import typing

from . import decorator
from .abc import set_stopped_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SetStopped(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    set_stopped_.SetStopped[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = SetStopped
set_stopped = SetStopped()
