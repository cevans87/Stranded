import dataclasses

from . import decorator
from .abc import upon_stopped_


@dataclasses.dataclass(frozen=True, kw_only=True)
class UponStopped(decorator.Decorator, upon_stopped_.Decorator): ...


Decorator = UponStopped
upon_stopped = UponStopped()
