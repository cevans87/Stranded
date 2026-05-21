import dataclasses

from . import decorator
from .abc import schedule_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Schedule(decorator.Decorator, schedule_.Decorator): ...


Decorator = Schedule
schedule = Schedule()
