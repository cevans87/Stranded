import dataclasses
import typing

from . import decorator
from .abc import schedule_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Schedule(
    decorator.Decorator[..., typing.Any],
    schedule_.Schedule[..., typing.Any],
): ...


Decorator = Schedule
schedule = Schedule()
