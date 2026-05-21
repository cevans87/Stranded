import dataclasses

from . import decorator
from .abc import schedule_from_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ScheduleFrom(decorator.Decorator, schedule_from_.Decorator): ...


Decorator = ScheduleFrom
schedule_from = ScheduleFrom()
