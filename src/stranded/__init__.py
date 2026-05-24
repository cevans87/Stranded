from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import abc
    from . import argparse
    from . import asyncio
    from . import builtins
    from . import decorator
    from .decorator import Decorator
    from . import execution
    from . import functools
    from . import inspect
    from . import logging
    from . import pathlib
    from . import sqlite3
    from . import threading
    from . import types
    from . import typing


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'abc': return _importlib.import_module('.abc', __name__)
        case 'argparse': return _importlib.import_module('.argparse', __name__)
        case 'asyncio': return _importlib.import_module('.asyncio', __name__)
        case 'builtins': return _importlib.import_module('.builtins', __name__)
        case 'decorator': return _importlib.import_module('.decorator', __name__)
        case 'Decorator': return _importlib.import_module('.decorator', __name__).Decorator
        case 'execution': return _importlib.import_module('.execution', __name__)
        case 'functools': return _importlib.import_module('.functools', __name__)
        case 'inspect': return _importlib.import_module('.inspect', __name__)
        case 'logging': return _importlib.import_module('.logging', __name__)
        case 'pathlib': return _importlib.import_module('.pathlib', __name__)
        case 'sqlite3': return _importlib.import_module('.sqlite3', __name__)
        case 'threading': return _importlib.import_module('.threading', __name__)
        case 'types': return _importlib.import_module('.types', __name__)
        case 'typing': return _importlib.import_module('.typing', __name__)
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'abc',
    'argparse',
    'asyncio',
    'builtins',
    'decorator',
    'Decorator',
    'execution',
    'functools',
    'inspect',
    'logging',
    'pathlib',
    'sqlite3',
    'threading',
    'types',
    'typing',
)