import dataclasses

from . import decorator
from .abc import just_stopped_


@dataclasses.dataclass(frozen=True, kw_only=True)
class JustStopped(decorator.Decorator, just_stopped_.Decorator): ...


Decorator = JustStopped
just_stopped = JustStopped()
