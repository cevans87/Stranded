from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import argument_parser_
    from .argument_parser_ import ArgumentParser


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'argument_parser_': return _importlib.import_module('.argument_parser_', __name__)
        case 'ArgumentParser': return _importlib.import_module('.argument_parser_', __name__).ArgumentParser
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'argument_parser_',
    'ArgumentParser',
)