from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import abc
    from . import argparse
    from . import asyncio
    from . import builtins
    from . import composer
    from .composer import Composer
    from . import functools
    from . import logging
    from . import scheduler
    from .scheduler import Scheduler
    from . import sqlite3
    from . import threading
    from . import types


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'abc': return _importlib.import_module('.abc', __name__)
        case 'argparse': return _importlib.import_module('.argparse', __name__)
        case 'asyncio': return _importlib.import_module('.asyncio', __name__)
        case 'builtins': return _importlib.import_module('.builtins', __name__)
        case 'composer': return _importlib.import_module('.composer', __name__)
        case 'Composer': return _importlib.import_module('.composer', __name__).Composer
        case 'functools': return _importlib.import_module('.functools', __name__)
        case 'logging': return _importlib.import_module('.logging', __name__)
        case 'scheduler': return _importlib.import_module('.scheduler', __name__)
        case 'Scheduler': return _importlib.import_module('.scheduler', __name__).Scheduler
        case 'sqlite3': return _importlib.import_module('.sqlite3', __name__)
        case 'threading': return _importlib.import_module('.threading', __name__)
        case 'types': return _importlib.import_module('.types', __name__)
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'abc',
    'argparse',
    'asyncio',
    'builtins',
    'composer',
    'Composer',
    'functools',
    'logging',
    'scheduler',
    'Scheduler',
    'sqlite3',
    'threading',
    'types',
)
