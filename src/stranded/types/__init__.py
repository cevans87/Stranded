import importlib as _importlib
import types as _types
import typing as _typing


@_typing.overload
def __getattr__(name: _typing.Literal['convert']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Convert']) -> 'type[stranded.types.convert.Convert]': ...
def __getattr__(name):
    match name:
        case 'convert': return _importlib.import_module('.convert', __name__)
        case 'Convert': return _importlib.import_module('.convert', __name__).Convert
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'convert',
    'Convert',
]
