import dataclasses

from . import decorator
from .abc import read_env_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ReadEnv(decorator.Decorator, read_env_.Decorator): ...


Decorator = ReadEnv
read_env = ReadEnv()
