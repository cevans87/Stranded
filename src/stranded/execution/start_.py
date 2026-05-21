import dataclasses

from . import decorator
from .abc import start_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Start(decorator.Decorator, start_.Decorator): ...


Decorator = Start
start = Start()
