import importlib as _importlib
import types as _types
import typing as _typing


@_typing.overload
def __getattr__(name: _typing.Literal['db']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Db']) -> 'type[stranded.sqlite3.abc.db.Db]': ...
def __getattr__(name):
    match name:
        case 'db': return _importlib.import_module('.db', __name__)
        case 'Db': return _importlib.import_module('.db', __name__).Db
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'db',
    'Db',
]
