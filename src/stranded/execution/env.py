import dataclasses

from . import decorator
from .abc import env


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, env.Decorator): ...


Env = Decorator
