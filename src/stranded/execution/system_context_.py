import dataclasses
import typing

from . import decorator
from .abc import system_context_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SystemContext(
    decorator.Decorator[..., typing.Any],
    system_context_.SystemContext[..., typing.Any],
): ...


Decorator = SystemContext
system_context = SystemContext()
