import dataclasses

from . import decorator
from .abc import stop_token_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StopToken(decorator.Decorator, stop_token_.Decorator): ...


Decorator = StopToken
stop_token = StopToken()
