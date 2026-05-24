import dataclasses
import typing

from .abc import retry_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    retry_.Retry[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = Retry
retry = Retry()
