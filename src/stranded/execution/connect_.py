import dataclasses

from . import decorator
from .abc import connect_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect(decorator.Decorator, connect_.Decorator): ...


Decorator = Connect
connect = Connect()
