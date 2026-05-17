import dataclasses
import typing

from ..abc import inline_scheduler
from . import scheduler


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class InlineScheduler(scheduler.Scheduler, inline_scheduler.InlineScheduler):
    def __call__[_Ret](self, fn: typing.Callable[[], _Ret]) -> _Ret:
        return fn()
