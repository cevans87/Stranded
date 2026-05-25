import dataclasses
import typing

from . import decorator
from .abc import prop_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Prop(
    decorator.Decorator[..., typing.Any],
    prop_.Prop[..., typing.Any],
): ...


Decorator = Prop
prop = Prop()
