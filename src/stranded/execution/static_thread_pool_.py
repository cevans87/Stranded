import dataclasses

from . import decorator
from .abc import static_thread_pool_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StaticThreadPool(decorator.Decorator, static_thread_pool_.Decorator): ...


Decorator = StaticThreadPool
static_thread_pool = StaticThreadPool()
