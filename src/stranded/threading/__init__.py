from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import composer, scheduler
    from .composer import Composer
    from .scheduler import Scheduler


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'composer': return _importlib.import_module('.composer', __name__)
        case 'Composer': return _importlib.import_module('.composer', __name__).Composer
        case 'scheduler': return _importlib.import_module('.scheduler', __name__)
        case 'Scheduler': return _importlib.import_module('.scheduler', __name__).Scheduler
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'composer',
    'Composer',
    'scheduler',
    'Scheduler',
)
