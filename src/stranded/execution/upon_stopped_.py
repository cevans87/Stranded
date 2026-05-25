import dataclasses
import typing

from . import decorator
from .abc import upon_stopped_


@dataclasses.dataclass(frozen=True, kw_only=True)
class UponStopped(
    decorator.Decorator[..., typing.Any],
    upon_stopped_.UponStopped[..., typing.Any],
): ...


Decorator = UponStopped
upon_stopped = UponStopped()
