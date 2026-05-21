import dataclasses

from . import decorator
from .abc import let_stopped_


@dataclasses.dataclass(frozen=True, kw_only=True)
class LetStopped(decorator.Decorator, let_stopped_.Decorator): ...


Decorator = LetStopped
let_stopped = LetStopped()
