from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import logger_
    from .logger_ import Logger


@_typing.overload
def __getattr__(name: _typing.Literal['logger_']) -> type[logger_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Logger']) -> type[Logger]: ...
def __getattr__(name):
    match name:
        case 'logger_': return _importlib.import_module('.logger_', __name__)
        case 'Logger': return _importlib.import_module('.logger_', __name__).Logger
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'logger_',
    'Logger',
)