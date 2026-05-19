import dataclasses

from . import decorator
from .abc import as_awaitable


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, as_awaitable.Decorator): ...


AsAwaitable = Decorator
