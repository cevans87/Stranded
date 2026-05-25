import dataclasses
import typing

from . import decorator
from .abc import just_stopped_


@dataclasses.dataclass(frozen=True, kw_only=True)
class JustStopped(
    decorator.Decorator[..., typing.Any],
    just_stopped_.JustStopped[..., typing.Any],
): ...


Decorator = JustStopped
just_stopped = JustStopped()
