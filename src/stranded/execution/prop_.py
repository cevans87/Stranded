import dataclasses
import typing

from . import decorator
from .abc import prop_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Prop(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    prop_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = Prop
prop = Prop()
