import dataclasses
import typing

from . import decorator
from .abc import continues_on_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ContinuesOn(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    continues_on_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = ContinuesOn
continues_on = ContinuesOn()
