import dataclasses

from . import decorator
from .abc import inplace_stop_token_


@dataclasses.dataclass(frozen=True, kw_only=True)
class InplaceStopToken(decorator.Decorator, inplace_stop_token_.Decorator): ...


Decorator = InplaceStopToken
inplace_stop_token = InplaceStopToken()
