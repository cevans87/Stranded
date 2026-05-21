import dataclasses

from . import decorator
from .abc import operation_state_


@dataclasses.dataclass(frozen=True, kw_only=True)
class OperationState(decorator.Decorator, operation_state_.Decorator): ...


Decorator = OperationState
operation_state = OperationState()
