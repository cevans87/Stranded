from __future__ import annotations

import asyncio
import dataclasses
import importlib
import inspect
import typing

from . import composer
from .abc import composer as composer_abc
from .abc import decorator
from .abc import scheduler as scheduler_


def _dispatch(self: scheduler_.Scheduler[typing.Any, typing.Any], target: typing.Any) -> typing.Any:
    if isinstance(target, composer_abc.Composed):
        return dataclasses.replace(
            target,
            decorateds=tuple(self(d) for d in target.decorateds),
        )
    flavor = 'asyncio' if inspect.iscoroutinefunction(target) else 'threading'
    parts = type(self).__module__.split('.')
    parts.insert(-1, flavor)
    module = importlib.import_module('.'.join(parts))
    cls = getattr(module, type(self).__name__)
    target_field_names = {f.name for f in dataclasses.fields(cls)}
    kwargs = {
        f.name: getattr(self, f.name)
        for f in dataclasses.fields(self)
        if f.name in target_field_names
    }
    return cls(**kwargs)(target)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheduler[**ParamT, RetT](scheduler_.Scheduler[ParamT, RetT]):
    decoratee_t: typing.ClassVar = decorator.Decoratee
    exit_t: typing.ClassVar = decorator.Exit
    enter_t: typing.ClassVar = decorator.Enter
    decorated_t: typing.ClassVar = decorator.Decorated
    composer_t: typing.ClassVar = composer.Composer

    # Union of flavor-specific fields. The dispatcher forwards only the fields
    # the target flavor's Scheduler actually accepts.
    max_workers: int | None = None
    thread_name_prefix: str = 'stranded'
    loop: asyncio.AbstractEventLoop | None = None

    def submit_sync(
        self,
        fn: typing.Callable[..., typing.Any],
        args: tuple[typing.Any, ...],
        kwargs: dict[str, typing.Any],
    ) -> typing.Any:
        raise NotImplementedError

    async def submit_async(
        self,
        fn: typing.Callable[..., typing.Any],
        args: tuple[typing.Any, ...],
        kwargs: dict[str, typing.Any],
    ) -> typing.Any:
        raise NotImplementedError

    def __call__[DecorateeT](self, target: DecorateeT) -> DecorateeT:  # type: ignore[override]
        return _dispatch(self, target)
