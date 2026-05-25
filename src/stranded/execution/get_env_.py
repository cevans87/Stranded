import dataclasses
import typing

from . import decorator
from .abc import get_env_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetEnv(
    decorator.Decorator[..., typing.Any],
    get_env_.GetEnv[..., typing.Any],
): ...


Decorator = GetEnv
get_env = GetEnv()
