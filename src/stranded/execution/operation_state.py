import dataclasses

from . import decorator
from .abc import operation_state


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, operation_state.Decorator): ...


OperationState = Decorator
