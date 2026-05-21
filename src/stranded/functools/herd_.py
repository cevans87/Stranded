import dataclasses

from .abc import herd_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Herd(decorator.Decorator, herd_.Decorator):
    @property
    def future_t(self) -> type:
        raise NotImplementedError(
            f'{type(self).__name__} is a dispatcher; future_t is provided by the threading or asyncio variant.'
        )


Decorator = Herd
herd = Herd()
