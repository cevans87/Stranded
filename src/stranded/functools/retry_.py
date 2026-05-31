import dataclasses
import typing

from .abc import retry_
from .. import composer


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry(
    composer.Composer[..., typing.Any],
    retry_.Retry[..., typing.Any],
): ...


Composer = Retry
retry = Retry()
