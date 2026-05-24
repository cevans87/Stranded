import dataclasses
import typing

from . import decorator
from .abc import ensure_started_


@dataclasses.dataclass(frozen=True, kw_only=True)
class EnsureStarted(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    ensure_started_.EnsureStarted[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = EnsureStarted
ensure_started = EnsureStarted()
