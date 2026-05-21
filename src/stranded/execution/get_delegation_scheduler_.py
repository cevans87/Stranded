import dataclasses

from . import decorator
from .abc import get_delegation_scheduler_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetDelegationScheduler(decorator.Decorator, get_delegation_scheduler_.Decorator): ...


Decorator = GetDelegationScheduler
get_delegation_scheduler = GetDelegationScheduler()
