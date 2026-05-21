import dataclasses

from . import decorator
from .abc import with_awaitable_senders_


@dataclasses.dataclass(frozen=True, kw_only=True)
class WithAwaitableSenders(decorator.Decorator, with_awaitable_senders_.Decorator): ...


Decorator = WithAwaitableSenders
with_awaitable_senders = WithAwaitableSenders()
