import dataclasses

from . import decorator
from .abc import as_awaitable_


@dataclasses.dataclass(frozen=True, kw_only=True)
class AsAwaitable(decorator.Decorator, as_awaitable_.Decorator): ...


Decorator = AsAwaitable
as_awaitable = AsAwaitable()
