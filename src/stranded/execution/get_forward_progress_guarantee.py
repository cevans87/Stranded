import dataclasses

from . import decorator
from .abc import get_forward_progress_guarantee


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, get_forward_progress_guarantee.Decorator): ...


GetForwardProgressGuarantee = Decorator
