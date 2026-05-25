import dataclasses
import typing

from . import decorator
from .abc import stop_callback_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StopCallback(
    decorator.Decorator[..., typing.Any],
    stop_callback_.StopCallback[..., typing.Any],
): ...


Decorator = StopCallback
stop_callback = StopCallback()
