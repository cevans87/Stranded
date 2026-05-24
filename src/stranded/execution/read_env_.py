import dataclasses
import typing

from . import decorator
from .abc import read_env_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ReadEnv(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    read_env_.ReadEnv[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = ReadEnv
read_env = ReadEnv()
