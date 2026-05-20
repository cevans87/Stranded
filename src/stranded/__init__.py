import importlib as _importlib
import types as _types
import typing as _typing


@_typing.overload
def __getattr__(name: _typing.Literal['abc']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['argparse']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['asyncio']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['builtins']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['decorator']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Decorator']) -> 'type[stranded.decorator.Decorator]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['execution']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['functools']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inspect']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['logging']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['pathlib']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['sqlite3']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['threading']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['types']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['typing']) -> _types.ModuleType: ...
def __getattr__(name):
    match name:
        case 'abc': return _importlib.import_module('.abc', __name__)
        case 'argparse': return _importlib.import_module('.argparse', __name__)
        case 'asyncio': return _importlib.import_module('.asyncio', __name__)
        case 'builtins': return _importlib.import_module('.builtins', __name__)
        case 'decorator': return _importlib.import_module('.decorator', __name__)
        case 'Decorator': return _importlib.import_module('.decorator', __name__).Decorator
        case 'execution': return _importlib.import_module('.execution', __name__)
        case 'functools': return _importlib.import_module('.functools', __name__)
        case 'inspect': return _importlib.import_module('.inspect', __name__)
        case 'logging': return _importlib.import_module('.logging', __name__)
        case 'pathlib': return _importlib.import_module('.pathlib', __name__)
        case 'sqlite3': return _importlib.import_module('.sqlite3', __name__)
        case 'threading': return _importlib.import_module('.threading', __name__)
        case 'types': return _importlib.import_module('.types', __name__)
        case 'typing': return _importlib.import_module('.typing', __name__)
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'abc',
    'argparse',
    'asyncio',
    'builtins',
    'decorator',
    'Decorator',
    'execution',
    'functools',
    'inspect',
    'logging',
    'pathlib',
    'sqlite3',
    'threading',
    'types',
    'typing',
]
