from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import exception_
    from .exception_ import Exception


@_typing.overload
def __getattr__(name: _typing.Literal['exception_']) -> type[exception_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Exception']) -> type[Exception]: ...
def __getattr__(name):
    match name:
        case 'exception_': return _importlib.import_module('.exception_', __name__)
        case 'Exception': return _importlib.import_module('.exception_', __name__).Exception
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'exception_',
    'Exception',
)
