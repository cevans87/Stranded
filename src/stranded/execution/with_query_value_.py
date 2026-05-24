import dataclasses
import typing

from . import decorator
from .abc import with_query_value_


@dataclasses.dataclass(frozen=True, kw_only=True)
class WithQueryValue(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    with_query_value_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = WithQueryValue
with_query_value = WithQueryValue()
