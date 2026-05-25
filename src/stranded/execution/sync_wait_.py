import dataclasses
import typing

from . import decorator
from .abc import sync_wait_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SyncWait(
    decorator.Decorator[..., typing.Any],
    sync_wait_.SyncWait[..., typing.Any],
): ...


Decorator = SyncWait
sync_wait = SyncWait()
