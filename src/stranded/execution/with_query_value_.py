import dataclasses
import typing

from . import decorator
from .abc import with_query_value_


@dataclasses.dataclass(frozen=True, kw_only=True)
class WithQueryValue(
    decorator.Decorator[..., typing.Any],
    with_query_value_.WithQueryValue[..., typing.Any],
): ...


Decorator = WithQueryValue
with_query_value = WithQueryValue()
