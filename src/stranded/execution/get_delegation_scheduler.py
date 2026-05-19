import dataclasses

from . import decorator
from .abc import get_delegation_scheduler


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, get_delegation_scheduler.Decorator): ...


GetDelegationScheduler = Decorator
