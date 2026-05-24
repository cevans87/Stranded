from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import decorator
    from .decorator import Decorator


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'decorator': return _importlib.import_module('.decorator', __name__)
        case 'Decorator': return _importlib.import_module('.decorator', __name__).Decorator
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'decorator',
    'Decorator',
)