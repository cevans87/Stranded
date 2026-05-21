import dataclasses

from . import decorator
from .abc import scheduler_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheduler(decorator.Decorator, scheduler_.Decorator): ...


Decorator = Scheduler
scheduler = Scheduler()
