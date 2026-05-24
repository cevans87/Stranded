import dataclasses
import typing

from . import decorator
from .abc import operation_state_


@dataclasses.dataclass(frozen=True, kw_only=True)
class OperationState(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    operation_state_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = OperationState
operation_state = OperationState()
