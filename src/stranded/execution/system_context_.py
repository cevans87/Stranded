import dataclasses
import typing

from . import decorator
from .abc import system_context_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SystemContext(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    system_context_.SystemContext[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = SystemContext
system_context = SystemContext()
