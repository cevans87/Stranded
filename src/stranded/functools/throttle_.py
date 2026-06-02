import dataclasses
import typing

from .abc import throttle_
from .. import composer_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Throttle(composer_.Composer[..., typing.Any], throttle_.Throttle[..., typing.Any]): ...


Composer = Throttle
throttle = Throttle()
