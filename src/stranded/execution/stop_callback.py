import dataclasses

from . import decorator
from .abc import stop_callback


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, stop_callback.Decorator): ...


StopCallback = Decorator
