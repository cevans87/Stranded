import dataclasses

from .abc_ import sqlite_cache
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class SqliteCache(decorator.Decorator, sqlite_cache.Decorator): ...
