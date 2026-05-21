import dataclasses

from . import decorator
from .abc import inplace_stop_callback_


@dataclasses.dataclass(frozen=True, kw_only=True)
class InplaceStopCallback(decorator.Decorator, inplace_stop_callback_.Decorator): ...


Decorator = InplaceStopCallback
inplace_stop_callback = InplaceStopCallback()
