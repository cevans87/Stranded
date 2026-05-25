import dataclasses
import typing

from . import decorator
from .abc import get_delegation_scheduler_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetDelegationScheduler(
    decorator.Decorator[..., typing.Any],
    get_delegation_scheduler_.GetDelegationScheduler[..., typing.Any],
): ...


Decorator = GetDelegationScheduler
get_delegation_scheduler = GetDelegationScheduler()
