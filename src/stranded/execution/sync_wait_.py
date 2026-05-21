import dataclasses

from . import decorator
from .abc import sync_wait_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SyncWait(decorator.Decorator, sync_wait_.Decorator): ...


Decorator = SyncWait
sync_wait = SyncWait()
