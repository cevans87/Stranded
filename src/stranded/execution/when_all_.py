import dataclasses

from . import decorator
from .abc import when_all_


@dataclasses.dataclass(frozen=True, kw_only=True)
class WhenAll(decorator.Decorator, when_all_.Decorator): ...


Decorator = WhenAll
when_all = WhenAll()
