import dataclasses

from . import decorator
from .abc import set_stopped_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SetStopped(decorator.Decorator, set_stopped_.Decorator): ...


Decorator = SetStopped
set_stopped = SetStopped()
