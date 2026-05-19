import dataclasses

from . import decorator
from .abc import never_stop_token


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, never_stop_token.Decorator): ...


NeverStopToken = Decorator
