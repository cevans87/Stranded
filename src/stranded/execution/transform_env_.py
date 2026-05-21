import dataclasses

from . import decorator
from .abc import transform_env_


@dataclasses.dataclass(frozen=True, kw_only=True)
class TransformEnv(decorator.Decorator, transform_env_.Decorator): ...


Decorator = TransformEnv
transform_env = TransformEnv()
