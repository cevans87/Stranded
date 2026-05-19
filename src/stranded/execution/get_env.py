import dataclasses

from . import decorator
from .abc import get_env


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, get_env.Decorator): ...


GetEnv = Decorator
