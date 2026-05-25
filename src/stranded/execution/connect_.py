import dataclasses
import typing

from . import decorator
from .abc import connect_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect(
    decorator.Decorator[..., typing.Any],
    connect_.Connect[..., typing.Any],
): ...


Decorator = Connect
connect = Connect()
