import dataclasses

from .abc_ import cache as abc_cache
from funktools import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Cache(decorator.Decorator, abc_cache.Decorator): ...
