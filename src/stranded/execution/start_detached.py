import dataclasses

from . import decorator
from .abc import start_detached


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, start_detached.Decorator): ...


StartDetached = Decorator
