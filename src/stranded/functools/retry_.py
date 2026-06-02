import dataclasses
import typing

from .abc import retry_
from .. import composer_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Retry(composer_.Composer[..., typing.Any], retry_.Retry[..., typing.Any]): ...


Composer = Retry
retry = Retry()
