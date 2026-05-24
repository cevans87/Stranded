import dataclasses
import typing

from . import decorator
from .abc import forwarding_query_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ForwardingQuery(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    forwarding_query_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = ForwardingQuery
forwarding_query = ForwardingQuery()
