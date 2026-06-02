from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import composer_
    from .composer_ import Composer


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'composer_': return _importlib.import_module('.composer_', __name__)
        case 'Composer': return _importlib.import_module('.composer_', __name__).Composer
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'composer_',
    'Composer',
)
