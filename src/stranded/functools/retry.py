import dataclasses

from .abc import retry
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry(decorator.Decorator, retry.Decorator): ...
