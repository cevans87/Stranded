import dataclasses
import typing

from . import decorator
from .abc import start_detached_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StartDetached(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    start_detached_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = StartDetached
start_detached = StartDetached()
