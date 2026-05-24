import dataclasses
import typing

from . import decorator
from .abc import let_stopped_


@dataclasses.dataclass(frozen=True, kw_only=True)
class LetStopped(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    let_stopped_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = LetStopped
let_stopped = LetStopped()
