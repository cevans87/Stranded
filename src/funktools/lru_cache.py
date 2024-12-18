import dataclasses

from .abc_ import lru_cache as abc_lru_cache
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache(decorator.Decorator, abc_lru_cache.Decorator): ...
