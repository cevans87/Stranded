import dataclasses

from . import decorator
from .abc import scheduler


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, scheduler.Decorator): ...


Scheduler = Decorator
