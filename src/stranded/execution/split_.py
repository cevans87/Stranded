import dataclasses

from . import decorator
from .abc import split_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Split(decorator.Decorator, split_.Decorator): ...


Decorator = Split
split = Split()
