import dataclasses

from .abc import lru_cache_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache(decorator.Decorator, lru_cache_.Decorator): ...


Decorator = LruCache
lru_cache = LruCache()
