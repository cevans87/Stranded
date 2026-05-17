import importlib as _importlib
import types as _types
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import bulk
    from .bulk import Bulk
    from . import inline_scheduler
    from .inline_scheduler import InlineScheduler
    from . import scheduler
    from .scheduler import Scheduler
    from . import stoppped
    from .stopped import Stopped
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
def __getattr__(name: _typing.Literal['inline_scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InlineScheduler']) -> type[InlineScheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Scheduler']) -> type[Scheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Stopped']) -> type[Stopped]: ...
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
        case 'inline_scheduler': return _importlib.import_module('.inline_scheduler', __name__)
        case 'InlineScheduler': return _importlib.import_module('.inline_scheduler', __name__).InlineScheduler
        case 'scheduler': return _importlib.import_module('.scheduler', __name__)
        case 'Scheduler': return _importlib.import_module('.scheduler', __name__).Scheduler
        case 'stopped': return _importlib.import_module('.stopped', __name__)
        case 'Stopped': return _importlib.import_module('.stopped', __name__).Stopped
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
    'inline_scheduler',
    'InlineScheduler',
    'scheduler',
    'Scheduler',
    'stopped',
    'Stopped',
    'then',
    'Then',
    'upon_error',
    'UponError',
    'upon_stopped',
    'UponStopped',
]
