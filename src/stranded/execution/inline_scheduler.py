import dataclasses
import inspect
import typing

from . import scheduler
from .asyncio import inline_scheduler as _asyncio_inline_scheduler
from .threading import inline_scheduler as _threading_inline_scheduler


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class InlineScheduler(
    scheduler.Scheduler,
    _threading_inline_scheduler.InlineScheduler,
    _asyncio_inline_scheduler.InlineScheduler,
):
    def __call__(self, fn):
        if inspect.iscoroutinefunction(fn):
            return _asyncio_inline_scheduler.InlineScheduler.__call__(self, fn)
        return _threading_inline_scheduler.InlineScheduler.__call__(self, fn)
