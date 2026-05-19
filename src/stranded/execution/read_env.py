import dataclasses

from . import decorator
from .abc import read_env


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, read_env.Decorator): ...


ReadEnv = Decorator
