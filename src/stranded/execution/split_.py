import dataclasses
import typing

from . import decorator
from .abc import split_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Split(
    decorator.Decorator[..., typing.Any],
    split_.Split[..., typing.Any],
): ...


Decorator = Split
split = Split()
