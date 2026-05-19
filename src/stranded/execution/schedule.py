import dataclasses

from . import decorator
from .abc import schedule


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, schedule.Decorator): ...


Schedule = Decorator
