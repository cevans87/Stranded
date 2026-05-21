import dataclasses

from . import decorator
from .abc import sync_wait_with_variant_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SyncWaitWithVariant(decorator.Decorator, sync_wait_with_variant_.Decorator): ...


Decorator = SyncWaitWithVariant
sync_wait_with_variant = SyncWaitWithVariant()
