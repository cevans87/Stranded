import dataclasses
import typing

from ..abc import inline_scheduler
from . import scheduler


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class InlineScheduler(scheduler.Scheduler, inline_scheduler.InlineScheduler):
    async def __call__[_Ret](self, coro_fn: typing.Callable[[], typing.Awaitable[_Ret]]) -> _Ret:
        return await coro_fn()
