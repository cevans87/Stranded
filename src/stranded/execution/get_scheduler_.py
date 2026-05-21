import dataclasses

from . import decorator
from .abc import get_scheduler_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetScheduler(decorator.Decorator, get_scheduler_.Decorator): ...


Decorator = GetScheduler
get_scheduler = GetScheduler()
