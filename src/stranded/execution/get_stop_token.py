import dataclasses

from . import decorator
from .abc import get_stop_token


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, get_stop_token.Decorator): ...


GetStopToken = Decorator
