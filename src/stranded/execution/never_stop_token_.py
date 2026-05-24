import dataclasses
import typing

from . import decorator
from .abc import never_stop_token_


@dataclasses.dataclass(frozen=True, kw_only=True)
class NeverStopToken(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    never_stop_token_.NeverStopToken[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = NeverStopToken
never_stop_token = NeverStopToken()
