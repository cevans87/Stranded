import dataclasses

from . import decorator
from .abc import system_context_


@dataclasses.dataclass(frozen=True, kw_only=True)
class SystemContext(decorator.Decorator, system_context_.Decorator): ...


Decorator = SystemContext
system_context = SystemContext()
