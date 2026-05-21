import dataclasses

from . import decorator
from .abc import never_stop_token_


@dataclasses.dataclass(frozen=True, kw_only=True)
class NeverStopToken(decorator.Decorator, never_stop_token_.Decorator): ...


Decorator = NeverStopToken
never_stop_token = NeverStopToken()
