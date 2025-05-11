import dataclasses

from .abc_ import lru_cache
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache(decorator.Decorator, lru_cache.Decorator): ...
