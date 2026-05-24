import dataclasses
import typing

from . import decorator
from .abc import get_completion_signatures_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetCompletionSignatures(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    get_completion_signatures_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = GetCompletionSignatures
get_completion_signatures = GetCompletionSignatures()
