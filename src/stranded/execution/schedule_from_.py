import dataclasses
import typing

from . import decorator
from .abc import schedule_from_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ScheduleFrom(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    schedule_from_.ScheduleFrom[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = ScheduleFrom
schedule_from = ScheduleFrom()
