import dataclasses
import typing

from . import decorator
from .abc import transform_env_


@dataclasses.dataclass(frozen=True, kw_only=True)
class TransformEnv(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    transform_env_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = TransformEnv
transform_env = TransformEnv()
