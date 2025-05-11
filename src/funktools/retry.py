import dataclasses

from .abc_ import retry
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry(decorator.Decorator, retry.Decorator): ...
