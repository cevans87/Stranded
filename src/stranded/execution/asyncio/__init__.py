import importlib as _importlib
import types as _types
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import bulk
    from .bulk import Bulk
    from . import then
    from .then import Then
    from . import upon_error
    from .upon_error import UponError
    from . import upon_stopped
    from .upon_stopped import UponStopped


@_typing.overload
def __getattr__(name: _typing.Literal['bulk']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Bulk']) -> type[Bulk]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['then']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Then']) -> type[Then]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['upon_error']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['UponError']) -> type[UponError]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['upon_stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['UponStopped']) -> type[UponStopped]: ...
def __getattr__(name):
    match name:
        case 'bulk': return _importlib.import_module('.bulk', __name__)
        case 'Bulk': return _importlib.import_module('.bulk', __name__).Bulk
        case 'then': return _importlib.import_module('.then', __name__)
        case 'Then': return _importlib.import_module('.then', __name__).Then
        case 'upon_error': return _importlib.import_module('.upon_error', __name__)
        case 'UponError': return _importlib.import_module('.upon_error', __name__).UponError
        case 'upon_stopped': return _importlib.import_module('.upon_stopped', __name__)
        case 'UponStopped': return _importlib.import_module('.upon_stopped', __name__).UponStopped
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'bulk',
    'Bulk',
    'then',
    'Then',
    'upon_error',
    'UponError',
    'upon_stopped',
    'UponStopped',
]
