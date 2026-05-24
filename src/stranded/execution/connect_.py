import dataclasses
import typing

from . import decorator
from .abc import connect_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    connect_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = Connect
connect = Connect()
