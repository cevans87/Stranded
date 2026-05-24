import dataclasses
import typing

from . import decorator
from .abc import get_forward_progress_guarantee_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetForwardProgressGuarantee(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    get_forward_progress_guarantee_.GetForwardProgressGuarantee[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = GetForwardProgressGuarantee
get_forward_progress_guarantee = GetForwardProgressGuarantee()
