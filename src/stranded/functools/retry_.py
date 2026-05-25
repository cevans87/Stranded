import dataclasses
import typing

from .abc import retry_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry(
    decorator.Decorator[..., typing.Any],
    retry_.Retry[..., typing.Any],
): ...


Decorator = Retry
retry = Retry()
