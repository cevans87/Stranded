import dataclasses

from . import decorator
from .abc import system_context


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, system_context.Decorator): ...


SystemContext = Decorator
