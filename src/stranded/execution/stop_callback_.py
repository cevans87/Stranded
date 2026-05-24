import dataclasses
import typing

from . import decorator
from .abc import stop_callback_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StopCallback(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    stop_callback_.StopCallback[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = StopCallback
stop_callback = StopCallback()
