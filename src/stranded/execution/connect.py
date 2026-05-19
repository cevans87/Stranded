import dataclasses

from . import decorator
from .abc import connect


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, connect.Decorator):
    """Binary CPO. `Connect()(sender, receiver)` returns the OperationState
    that the sender builds when asked to connect with the receiver.

    Does not follow the unary Decoratee/Decorated flow: connecting two
    distinct things isn't a decoration, it's a composition. The sender
    provides the implementation via its `connect` method; Connect is
    just the dispatch entry point.
    """

    def __call__(self, sender, receiver, /):
        return sender.connect(receiver)


Connect = Decorator
