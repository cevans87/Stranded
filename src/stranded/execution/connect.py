import dataclasses

from . import decorator
from .abc import connect


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, connect.Decorator): ...


Connect = Decorator
