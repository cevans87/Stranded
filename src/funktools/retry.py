import dataclasses

from .abc_ import retry as abc_retry
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry(decorator.Decorator, abc_retry.Decorator): ...
