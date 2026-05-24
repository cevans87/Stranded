import dataclasses
import typing

from . import decorator
from .abc import stop_token_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StopToken(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    stop_token_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = StopToken
stop_token = StopToken()
