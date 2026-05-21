import dataclasses

from . import decorator
from .abc import inline_scheduler_


@dataclasses.dataclass(frozen=True, kw_only=True)
class InlineScheduler(decorator.Decorator, inline_scheduler_.Decorator): ...


Decorator = InlineScheduler
inline_scheduler = InlineScheduler()
