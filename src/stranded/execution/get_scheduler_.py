import dataclasses
import typing

from . import decorator
from .abc import get_scheduler_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetScheduler(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    get_scheduler_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = GetScheduler
get_scheduler = GetScheduler()
