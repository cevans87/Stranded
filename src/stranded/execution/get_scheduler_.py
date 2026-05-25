import dataclasses
import typing

from . import decorator
from .abc import get_scheduler_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetScheduler(
    decorator.Decorator[..., typing.Any],
    get_scheduler_.GetScheduler[..., typing.Any],
): ...


Decorator = GetScheduler
get_scheduler = GetScheduler()
