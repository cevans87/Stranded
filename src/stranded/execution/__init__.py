from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import abc
    from . import asyncio
    from . import scheduler_
    from .scheduler_ import Scheduler
    from . import threading


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'abc': return _importlib.import_module('.abc', __name__)
        case 'asyncio': return _importlib.import_module('.asyncio', __name__)
        case 'scheduler_': return _importlib.import_module('.scheduler_', __name__)
        case 'Scheduler': return _importlib.import_module('.scheduler_', __name__).Scheduler
        case 'threading': return _importlib.import_module('.threading', __name__)
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'abc',
    'asyncio',
    'scheduler_',
    'Scheduler',
    'threading',
)
