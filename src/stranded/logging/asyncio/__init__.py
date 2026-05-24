from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import logger_
    from .logger_ import Logger


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'logger_': return _importlib.import_module('.logger_', __name__)
        case 'Logger': return _importlib.import_module('.logger_', __name__).Logger
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'logger_',
    'Logger',
)