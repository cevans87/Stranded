import dataclasses
import typing

from . import decorator
from .abc import static_thread_pool_


@dataclasses.dataclass(frozen=True, kw_only=True)
class StaticThreadPool(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    static_thread_pool_.StaticThreadPool[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = StaticThreadPool
static_thread_pool = StaticThreadPool()
