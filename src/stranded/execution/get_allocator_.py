import dataclasses
import typing

from . import decorator
from .abc import get_allocator_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetAllocator(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    get_allocator_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = GetAllocator
get_allocator = GetAllocator()
