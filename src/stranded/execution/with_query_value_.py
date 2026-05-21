import dataclasses

from . import decorator
from .abc import with_query_value_


@dataclasses.dataclass(frozen=True, kw_only=True)
class WithQueryValue(decorator.Decorator, with_query_value_.Decorator): ...


Decorator = WithQueryValue
with_query_value = WithQueryValue()
