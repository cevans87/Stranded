import dataclasses

from . import decorator
from .abc import let_value


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, let_value.Decorator): ...


LetValue = Decorator
