import dataclasses

from . import decorator
from .abc import inline_scheduler


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, inline_scheduler.Decorator): ...


InlineScheduler = Decorator
