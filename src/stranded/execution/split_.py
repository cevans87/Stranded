import dataclasses
import typing

from . import decorator
from .abc import split_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Split(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    split_.Split[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = Split
split = Split()
