import dataclasses

from . import decorator
from .abc import schedule_from


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, schedule_from.Decorator): ...


ScheduleFrom = Decorator
