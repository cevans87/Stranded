import dataclasses
import typing

from . import decorator
from .abc import get_completion_scheduler_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetCompletionScheduler(
    decorator.Decorator[..., typing.Any],
    get_completion_scheduler_.GetCompletionScheduler[..., typing.Any],
): ...


Decorator = GetCompletionScheduler
get_completion_scheduler = GetCompletionScheduler()
