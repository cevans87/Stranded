import dataclasses

from . import decorator
from .abc import stop_callback_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StopCallback(decorator.Decorator, stop_callback_.Decorator): ...


Decorator = StopCallback
stop_callback = StopCallback()
