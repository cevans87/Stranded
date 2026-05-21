import dataclasses

from . import decorator
from .abc import get_stop_token_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetStopToken(decorator.Decorator, get_stop_token_.Decorator): ...


Decorator = GetStopToken
get_stop_token = GetStopToken()
