from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import lru_cache_
    from .lru_cache_ import LruCache
    from .lru_cache_ import lru_cache
    from . import retry_
    from .retry_ import Retry
    from .retry_ import retry
    from . import throttle_
    from .throttle_ import Throttle
    from .throttle_ import throttle


@_typing.overload
def __getattr__(name: _typing.Literal['lru_cache_']) -> type[lru_cache_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['LruCache']) -> type[LruCache]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['lru_cache']) -> type[lru_cache]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['retry_']) -> type[retry_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Retry']) -> type[Retry]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['retry']) -> type[retry]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['throttle_']) -> type[throttle_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Throttle']) -> type[Throttle]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['throttle']) -> type[throttle]: ...
def __getattr__(name):
    match name:
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
