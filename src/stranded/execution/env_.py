import dataclasses
import typing

from . import decorator
from .abc import env_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Env(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    env_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = Env
env = Env()
