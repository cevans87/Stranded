import dataclasses
import typing

from . import decorator
from .abc import start_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Start(
    decorator.Decorator[..., typing.Any],
    start_.Start[..., typing.Any],
): ...


Decorator = Start
start = Start()
