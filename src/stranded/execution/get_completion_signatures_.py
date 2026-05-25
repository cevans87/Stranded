import dataclasses
import typing

from . import decorator
from .abc import get_completion_signatures_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetCompletionSignatures(
    decorator.Decorator[..., typing.Any],
    get_completion_signatures_.GetCompletionSignatures[..., typing.Any],
): ...


Decorator = GetCompletionSignatures
get_completion_signatures = GetCompletionSignatures()
