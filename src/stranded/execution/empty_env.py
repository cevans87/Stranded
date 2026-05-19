import dataclasses

from . import decorator
from .abc import empty_env


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, empty_env.Decorator): ...


EmptyEnv = Decorator
