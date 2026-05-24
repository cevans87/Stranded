import dataclasses
import typing

from . import decorator
from .abc import starts_on_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StartsOn(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    starts_on_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = StartsOn
starts_on = StartsOn()
