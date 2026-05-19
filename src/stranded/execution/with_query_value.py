import dataclasses

from . import decorator
from .abc import with_query_value


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, with_query_value.Decorator): ...


WithQueryValue = Decorator
