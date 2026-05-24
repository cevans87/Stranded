import dataclasses
import typing

from . import decorator
from .abc import inplace_stop_token_


@dataclasses.dataclass(frozen=True, kw_only=True)
class InplaceStopToken(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    inplace_stop_token_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = InplaceStopToken
inplace_stop_token = InplaceStopToken()
