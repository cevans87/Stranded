import dataclasses

from . import decorator
from .abc import with_awaitable_senders


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, with_awaitable_senders.Decorator): ...


WithAwaitableSenders = Decorator
