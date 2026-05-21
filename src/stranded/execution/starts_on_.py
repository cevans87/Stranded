import dataclasses

from . import decorator
from .abc import starts_on_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StartsOn(decorator.Decorator, starts_on_.Decorator): ...


Decorator = StartsOn
starts_on = StartsOn()
