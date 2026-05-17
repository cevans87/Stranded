import dataclasses

from .abc import retry
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, retry.Decorator): ...


Retry = Decorator
