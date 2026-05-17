import dataclasses

from .abc import lru_cache
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, lru_cache.Decorator): ...


LruCache = Decorator
