import dataclasses

from . import decorator
from .abc import forwarding_query_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ForwardingQuery(decorator.Decorator, forwarding_query_.Decorator): ...


Decorator = ForwardingQuery
forwarding_query = ForwardingQuery()
