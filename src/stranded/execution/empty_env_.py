import dataclasses
import typing

from . import decorator
from .abc import empty_env_


@dataclasses.dataclass(frozen=True, kw_only=True)
class EmptyEnv(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    empty_env_.EmptyEnv[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = EmptyEnv
empty_env = EmptyEnv()
