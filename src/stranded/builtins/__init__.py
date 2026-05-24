from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import exception_
    from .exception_ import Exception


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'exception_': return _importlib.import_module('.exception_', __name__)
        case 'Exception': return _importlib.import_module('.exception_', __name__).Exception
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'exception_',
    'Exception',
)
