import dataclasses

from . import decorator
from .abc import run_loop


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, run_loop.Decorator): ...


RunLoop = Decorator
