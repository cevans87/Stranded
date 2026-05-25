import dataclasses
import typing

from . import decorator
from .abc import as_awaitable_


@dataclasses.dataclass(frozen=True, kw_only=True)
class AsAwaitable(
    decorator.Decorator[..., typing.Any],
    as_awaitable_.AsAwaitable[..., typing.Any],
): ...


Decorator = AsAwaitable
as_awaitable = AsAwaitable()
