import dataclasses
import typing

from .abc import herd_
from .. import composer_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Herd(composer_.Composer[..., typing.Any], herd_.Herd[..., typing.Any]):
    @property
    def future_t(self) -> type:
        raise NotImplementedError(
            f'{type(self).__name__} is a dispatcher; future_t is provided by the threading or asyncio variant.'
        )


Composer = Herd
herd = Herd()
