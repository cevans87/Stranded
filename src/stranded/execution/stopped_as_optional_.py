import dataclasses
import typing

from . import decorator
from .abc import stopped_as_optional_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StoppedAsOptional(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    stopped_as_optional_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = StoppedAsOptional
stopped_as_optional = StoppedAsOptional()
