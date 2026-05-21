import dataclasses

from .abc import herd_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Herd(decorator.Decorator, herd_.Decorator): ...


Decorator = Herd
herd = Herd()
