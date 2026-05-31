import dataclasses
import typing

from .abc import throttle_
from .. import composer


@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle(composer.Composer[..., typing.Any], throttle_.Throttle[..., typing.Any]): ...


Composer = Throttle
throttle = Throttle()
