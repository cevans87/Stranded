import dataclasses

from . import decorator
from .abc import sync_wait


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, sync_wait.Decorator): ...


SyncWait = Decorator
