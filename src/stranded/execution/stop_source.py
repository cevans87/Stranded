import dataclasses

from . import decorator
from .abc import stop_source


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, stop_source.Decorator): ...


StopSource = Decorator
