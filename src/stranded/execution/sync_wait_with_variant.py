import dataclasses

from . import decorator
from .abc import sync_wait_with_variant


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, sync_wait_with_variant.Decorator): ...


SyncWaitWithVariant = Decorator
