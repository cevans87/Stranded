import dataclasses

from . import decorator
from .abc import inplace_stop_token


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, inplace_stop_token.Decorator): ...


InplaceStopToken = Decorator
