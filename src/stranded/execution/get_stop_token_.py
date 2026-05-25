import dataclasses
import typing

from . import decorator
from .abc import get_stop_token_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetStopToken(
    decorator.Decorator[..., typing.Any],
    get_stop_token_.GetStopToken[..., typing.Any],
): ...


Decorator = GetStopToken
get_stop_token = GetStopToken()
