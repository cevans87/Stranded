import dataclasses

from . import decorator
from .abc import inplace_stop_callback


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, inplace_stop_callback.Decorator): ...


InplaceStopCallback = Decorator
