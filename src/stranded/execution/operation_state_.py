import dataclasses
import typing

from . import decorator
from .abc import operation_state_


@dataclasses.dataclass(frozen=True, kw_only=True)
class OperationState(
    decorator.Decorator[..., typing.Any],
    operation_state_.OperationState[..., typing.Any],
): ...


Decorator = OperationState
operation_state = OperationState()
