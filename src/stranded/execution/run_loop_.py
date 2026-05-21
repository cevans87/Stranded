import dataclasses

from . import decorator
from .abc import run_loop_


@dataclasses.dataclass(frozen=True, kw_only=True)
class RunLoop(decorator.Decorator, run_loop_.Decorator): ...


Decorator = RunLoop
run_loop = RunLoop()
