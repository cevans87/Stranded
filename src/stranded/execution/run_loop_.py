import dataclasses
import typing

from . import decorator
from .abc import run_loop_


@dataclasses.dataclass(frozen=True, kw_only=True)
class RunLoop(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    run_loop_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = RunLoop
run_loop = RunLoop()
