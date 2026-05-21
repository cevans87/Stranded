import dataclasses

from . import decorator
from .abc import get_forward_progress_guarantee_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetForwardProgressGuarantee(decorator.Decorator, get_forward_progress_guarantee_.Decorator): ...


Decorator = GetForwardProgressGuarantee
get_forward_progress_guarantee = GetForwardProgressGuarantee()
