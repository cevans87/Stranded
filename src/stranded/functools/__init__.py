from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import herd_
    from .herd_ import Herd
    from .herd_ import herd
    from . import lru_cache_
    from .lru_cache_ import LruCache
    from .lru_cache_ import lru_cache
    from . import retry_
    from .retry_ import Retry
    from .retry_ import retry
    from . import throttle_
    from .throttle_ import Throttle
    from .throttle_ import throttle


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'herd_': return _importlib.import_module('.herd_', __name__)
        case 'Herd': return _importlib.import_module('.herd_', __name__).Herd
        case 'herd': return _importlib.import_module('.herd_', __name__).herd
        case 'lru_cache_': return _importlib.import_module('.lru_cache_', __name__)
        case 'LruCache': return _importlib.import_module('.lru_cache_', __name__).LruCache
        case 'lru_cache': return _importlib.import_module('.lru_cache_', __name__).lru_cache
        case 'retry_': return _importlib.import_module('.retry_', __name__)
        case 'Retry': return _importlib.import_module('.retry_', __name__).Retry
        case 'retry': return _importlib.import_module('.retry_', __name__).retry
        case 'throttle_': return _importlib.import_module('.throttle_', __name__)
        case 'Throttle': return _importlib.import_module('.throttle_', __name__).Throttle
        case 'throttle': return _importlib.import_module('.throttle_', __name__).throttle
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'herd_',
    'Herd',
    'herd',
    'lru_cache_',
    'LruCache',
    'lru_cache',
    'retry_',
    'Retry',
    'retry',
    'throttle_',
    'Throttle',
    'throttle',
)
