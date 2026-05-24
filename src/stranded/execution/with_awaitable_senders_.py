import dataclasses
import typing

from . import decorator
from .abc import with_awaitable_senders_


@dataclasses.dataclass(frozen=True, kw_only=True)
class WithAwaitableSenders(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    with_awaitable_senders_.WithAwaitableSenders[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = WithAwaitableSenders
with_awaitable_senders = WithAwaitableSenders()
