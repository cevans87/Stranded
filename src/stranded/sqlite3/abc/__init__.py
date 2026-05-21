from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import db_
    from .db_ import Db
    from .db_ import db


@_typing.overload
def __getattr__(name: _typing.Literal['db_']) -> type[db_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Db']) -> type[Db]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['db']) -> type[db]: ...
def __getattr__(name):
    match name:
        case 'db_': return _importlib.import_module('.db_', __name__)
        case 'Db': return _importlib.import_module('.db_', __name__).Db
        case 'db': return _importlib.import_module('.db_', __name__).db
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'db_',
    'Db',
    'db',
)