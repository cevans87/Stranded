import dataclasses
import typing

from . import decorator
from .abc import sync_wait_with_variant_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SyncWaitWithVariant(
    decorator.Decorator[..., typing.Any],
    sync_wait_with_variant_.SyncWaitWithVariant[..., typing.Any],
): ...


Decorator = SyncWaitWithVariant
sync_wait_with_variant = SyncWaitWithVariant()
