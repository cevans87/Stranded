import dataclasses

from . import decorator
from .abc import continues_on


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, continues_on.Decorator): ...


ContinuesOn = Decorator
