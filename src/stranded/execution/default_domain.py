import dataclasses

from . import decorator
from .abc import default_domain


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, default_domain.Decorator): ...


DefaultDomain = Decorator
