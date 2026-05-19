import dataclasses

from . import decorator
from .abc import forwarding_query


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, forwarding_query.Decorator): ...


ForwardingQuery = Decorator
