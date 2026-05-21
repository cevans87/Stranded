import dataclasses

from . import decorator
from .abc import then_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Then(decorator.Decorator, then_.Decorator): ...


Decorator = Then
then = Then()
