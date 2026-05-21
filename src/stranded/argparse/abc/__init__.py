from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import argument_parser_
    from .argument_parser_ import ArgumentParser


@_typing.overload
def __getattr__(name: _typing.Literal['argument_parser_']) -> type[argument_parser_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ArgumentParser']) -> type[ArgumentParser]: ...
def __getattr__(name):
    match name:
        case 'argument_parser_': return _importlib.import_module('.argument_parser_', __name__)
        case 'ArgumentParser': return _importlib.import_module('.argument_parser_', __name__).ArgumentParser
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'argument_parser_',
    'ArgumentParser',
)