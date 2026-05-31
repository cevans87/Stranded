from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import decorator, scheduler
    from .decorator import Decorator
    from .scheduler import Scheduler


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'decorator': return _importlib.import_module('.decorator', __name__)
        case 'Decorator': return _importlib.import_module('.decorator', __name__).Decorator
        case 'scheduler': return _importlib.import_module('.scheduler', __name__)
        case 'Scheduler': return _importlib.import_module('.scheduler', __name__).Scheduler
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'decorator',
    'Decorator',
    'scheduler',
    'Scheduler',
)
