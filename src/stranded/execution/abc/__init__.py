from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import scheduler_
    from .scheduler_ import Scheduler


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'scheduler_': return _importlib.import_module('.scheduler_', __name__)
        case 'Scheduler': return _importlib.import_module('.scheduler_', __name__).Scheduler
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'scheduler_',
    'Scheduler',
)
