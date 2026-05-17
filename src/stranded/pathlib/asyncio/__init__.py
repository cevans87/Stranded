import importlib as _importlib
import types as _types
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import path
    from .path import Path


@_typing.overload
def __getattr__(name: _typing.Literal['path']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Path']) -> type[Path]: ...
def __getattr__(name):
    match name:
        case 'path': return _importlib.import_module('.path', __name__)
        case 'Path': return _importlib.import_module('.path', __name__).Path
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'path',
    'Path',
]
