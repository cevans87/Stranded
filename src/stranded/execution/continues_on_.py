import dataclasses

from . import decorator
from .abc import continues_on_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ContinuesOn(decorator.Decorator, continues_on_.Decorator): ...


Decorator = ContinuesOn
continues_on = ContinuesOn()
