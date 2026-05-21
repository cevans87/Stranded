import dataclasses

from . import decorator
from .abc import get_completion_scheduler_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetCompletionScheduler(decorator.Decorator, get_completion_scheduler_.Decorator): ...


Decorator = GetCompletionScheduler
get_completion_scheduler = GetCompletionScheduler()
