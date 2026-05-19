import dataclasses

from . import decorator
from .abc import stop_token


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, stop_token.Decorator): ...


StopToken = Decorator
