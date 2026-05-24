import dataclasses
import typing

from . import decorator
from .abc import inplace_stop_callback_


@dataclasses.dataclass(frozen=True, kw_only=True)
class InplaceStopCallback(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    inplace_stop_callback_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = InplaceStopCallback
inplace_stop_callback = InplaceStopCallback()
