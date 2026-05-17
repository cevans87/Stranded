import importlib as _importlib
import types as _types
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import decorator
    from .decorator import Decorator


@_typing.overload
def __getattr__(name: _typing.Literal['decorator']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Decorator']) -> type[Decorator]: ...
def __getattr__(name):
    match name:
        case 'decorator': return _importlib.import_module('.decorator', __name__)
        case 'Decorator': return _importlib.import_module('.decorator', __name__).Decorator
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'decorator',
    'Decorator',
]
