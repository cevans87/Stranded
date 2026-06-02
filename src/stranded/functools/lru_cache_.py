import dataclasses
import typing

from .abc import lru_cache_
from .. import composer_


@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache(composer_.Composer[..., typing.Any], lru_cache_.LruCache[..., typing.Any]):
    @property
    def future_t(self) -> type:
        raise NotImplementedError(
            f'{type(self).__name__} is a dispatcher; future_t is provided by the threading or asyncio variant.'
        )


Composer = LruCache
lru_cache = LruCache()
