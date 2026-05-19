import dataclasses

from . import decorator
from .abc import get_domain


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, get_domain.Decorator): ...


GetDomain = Decorator
