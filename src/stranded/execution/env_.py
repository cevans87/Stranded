import dataclasses

from . import decorator
from .abc import env_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Env(decorator.Decorator, env_.Decorator): ...


Decorator = Env
env = Env()
