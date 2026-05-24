from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import convert
    from .convert import Convert


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'convert': return _importlib.import_module('.convert', __name__)
        case 'Convert': return _importlib.import_module('.convert', __name__).Convert
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'convert',
    'Convert',
)