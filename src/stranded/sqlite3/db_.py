import dataclasses
import typing

from .. import decorator
from .abc import db_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Db(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    db_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = Db
db = Db()
