import dataclasses

from . import decorator
from .abc import static_thread_pool


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator, static_thread_pool.Decorator): ...


StaticThreadPool = Decorator
