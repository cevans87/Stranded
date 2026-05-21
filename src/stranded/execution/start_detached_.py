import dataclasses

from . import decorator
from .abc import start_detached_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StartDetached(decorator.Decorator, start_detached_.Decorator): ...


Decorator = StartDetached
start_detached = StartDetached()
