import dataclasses

from .abc import lru_cache_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache(decorator.Decorator, lru_cache_.Decorator):
    @property
    def future_t(self) -> type:
        raise NotImplementedError(
            f'{type(self).__name__} is a dispatcher; future_t is provided by the threading or asyncio variant.'
        )


Decorator = LruCache
lru_cache = LruCache()
