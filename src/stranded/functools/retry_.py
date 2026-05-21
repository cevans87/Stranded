import dataclasses

from .abc import retry_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry(decorator.Decorator, retry_.Decorator): ...


Decorator = Retry
retry = Retry()
