import dataclasses
import typing

from .abc import throttle_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    throttle_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = Throttle
throttle = Throttle()
