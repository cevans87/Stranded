import importlib as _importlib
import types as _types
import typing as _typing


@_typing.overload
def __getattr__(name: _typing.Literal['logger']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Logger']) -> 'type[stranded.logging.abc.logger.Logger]': ...
def __getattr__(name):
    match name:
        case 'logger': return _importlib.import_module('.logger', __name__)
        case 'Logger': return _importlib.import_module('.logger', __name__).Logger
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'logger',
    'Logger',
]
