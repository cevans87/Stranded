import dataclasses

from . import decorator
from .abc import get_allocator_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetAllocator(decorator.Decorator, get_allocator_.Decorator): ...


Decorator = GetAllocator
get_allocator = GetAllocator()
