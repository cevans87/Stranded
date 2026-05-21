import dataclasses

from . import decorator
from .abc import get_env_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetEnv(decorator.Decorator, get_env_.Decorator): ...


Decorator = GetEnv
get_env = GetEnv()
