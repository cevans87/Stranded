import dataclasses
import typing

from . import decorator
from .abc import inline_scheduler_


@dataclasses.dataclass(frozen=True, kw_only=True)
class InlineScheduler(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    inline_scheduler_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = InlineScheduler
inline_scheduler = InlineScheduler()
