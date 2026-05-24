import dataclasses
import typing

from . import decorator
from .abc import scheduler_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheduler(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    scheduler_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = Scheduler
scheduler = Scheduler()
