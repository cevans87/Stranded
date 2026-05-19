import dataclasses

from . import decorator
from .abc import set_value


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, set_value.Decorator): ...


SetValue = Decorator
