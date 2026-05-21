from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import convert
    from .convert import Convert


@_typing.overload
def __getattr__(name: _typing.Literal['convert']) -> type[convert]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Convert']) -> type[Convert]: ...
def __getattr__(name):
    match name:
        case 'convert': return _importlib.import_module('.convert', __name__)
        case 'Convert': return _importlib.import_module('.convert', __name__).Convert
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'convert',
    'Convert',
)