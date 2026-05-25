import dataclasses
import typing

from .abc import throttle_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle(
    decorator.Decorator[..., typing.Any],
    throttle_.Throttle[..., typing.Any],
): ...


Decorator = Throttle
throttle = Throttle()
