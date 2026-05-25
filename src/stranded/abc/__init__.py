from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import composer, decorator
    from .composer import Composer
    from .decorator import Decorator


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'composer': return _importlib.import_module('.composer', __name__)
        case 'Composer': return _importlib.import_module('.composer', __name__).Composer
        case 'decorator': return _importlib.import_module('.decorator', __name__)
        case 'Decorator': return _importlib.import_module('.decorator', __name__).Decorator
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'composer',
    'Composer',
    'decorator',
    'Decorator',
)
