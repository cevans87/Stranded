import dataclasses

from .asyncio import scheduler as _asyncio_scheduler
from .threading import scheduler as _threading_scheduler


@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheduler(_threading_scheduler.Scheduler, _asyncio_scheduler.Scheduler): ...
