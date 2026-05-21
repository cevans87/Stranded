import dataclasses

from . import decorator
from .abc import empty_env_


@dataclasses.dataclass(frozen=True, kw_only=True)
class EmptyEnv(decorator.Decorator, empty_env_.Decorator): ...


Decorator = EmptyEnv
empty_env = EmptyEnv()
