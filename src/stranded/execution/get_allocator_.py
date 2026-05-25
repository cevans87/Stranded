import dataclasses
import typing

from . import decorator
from .abc import get_allocator_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetAllocator(
    decorator.Decorator[..., typing.Any],
    get_allocator_.GetAllocator[..., typing.Any],
): ...


Decorator = GetAllocator
get_allocator = GetAllocator()
