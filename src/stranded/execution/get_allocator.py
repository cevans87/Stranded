import dataclasses

from . import decorator
from .abc import get_allocator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, get_allocator.Decorator): ...


GetAllocator = Decorator
