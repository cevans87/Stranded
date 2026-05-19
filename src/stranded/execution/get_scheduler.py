import dataclasses

from . import decorator
from .abc import get_scheduler


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, get_scheduler.Decorator): ...


GetScheduler = Decorator
