import dataclasses

from . import decorator
from .abc import prop_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Prop(decorator.Decorator, prop_.Decorator): ...


Decorator = Prop
prop = Prop()
