import dataclasses

from . import decorator
from .abc import get_completion_signatures_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetCompletionSignatures(decorator.Decorator, get_completion_signatures_.Decorator): ...


Decorator = GetCompletionSignatures
get_completion_signatures = GetCompletionSignatures()
