import importlib as _importlib
import types as _types
import typing as _typing


@_typing.overload
def __getattr__(name: _typing.Literal['argument_parser']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ArgumentParser']) -> 'type[stranded.argparse.asyncio.argument_parser.ArgumentParser]': ...
def __getattr__(name):
    match name:
        case 'argument_parser': return _importlib.import_module('.argument_parser', __name__)
        case 'ArgumentParser': return _importlib.import_module('.argument_parser', __name__).ArgumentParser
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'argument_parser',
    'ArgumentParser',
]
