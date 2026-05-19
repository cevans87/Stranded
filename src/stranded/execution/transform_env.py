import dataclasses

from . import decorator
from .abc import transform_env


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, transform_env.Decorator): ...


TransformEnv = Decorator
