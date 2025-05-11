import dataclasses

from ..funktools import decorator
from .abc_ import cache


@dataclasses.dataclass(frozen=True, kw_only=True)
class Cache(decorator.Decorator, cache.Decorator): ...
