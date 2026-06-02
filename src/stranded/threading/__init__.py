from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import composer_, scheduler_
    from .composer_ import Composer
    from .scheduler_ import Scheduler


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'composer_': return _importlib.import_module('.composer_', __name__)
        case 'Composer': return _importlib.import_module('.composer_', __name__).Composer
        case 'scheduler_': return _importlib.import_module('.scheduler_', __name__)
        case 'Scheduler': return _importlib.import_module('.scheduler_', __name__).Scheduler
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'composer_',
    'Composer',
    'scheduler_',
    'Scheduler',
)
