import dataclasses
import typing

from . import decorator
from .abc import then_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Then(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    then_.Then[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = Then
then = Then()
