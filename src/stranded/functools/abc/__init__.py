import importlib as _importlib
import types as _types
import typing as _typing


@_typing.overload
def __getattr__(name: _typing.Literal['lru_cache']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['LruCache']) -> 'type[stranded.functools.abc.lru_cache.LruCache]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['retry']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Retry']) -> 'type[stranded.functools.abc.retry.Retry]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['throttle']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Throttle']) -> 'type[stranded.functools.abc.throttle.Throttle]': ...
def __getattr__(name):
    match name:
        case 'lru_cache': return _importlib.import_module('.lru_cache', __name__)
        case 'LruCache': return _importlib.import_module('.lru_cache', __name__).LruCache
        case 'retry': return _importlib.import_module('.retry', __name__)
        case 'Retry': return _importlib.import_module('.retry', __name__).Retry
        case 'throttle': return _importlib.import_module('.throttle', __name__)
        case 'Throttle': return _importlib.import_module('.throttle', __name__).Throttle
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'lru_cache',
    'LruCache',
    'retry',
    'Retry',
    'throttle',
    'Throttle',
]
