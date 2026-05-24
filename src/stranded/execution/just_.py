import dataclasses
import typing

from . import decorator
from .abc import just_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Just(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    just_.Just[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = Just
just = Just()
