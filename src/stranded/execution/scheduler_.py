from __future__ import annotations

import asyncio
import dataclasses
import importlib
import inspect
import typing

from ..abc import composer_
from .abc import scheduler_


def _dispatch(self: scheduler_.Scheduler[typing.Any, typing.Any], target: typing.Any) -> typing.Any:
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
    Composee: typing.ClassVar = composer_.Composee
    Connect: typing.ClassVar = composer_.Connect
    Exit: typing.ClassVar = composer_.Exit
    Enter: typing.ClassVar = composer_.Enter
    Composed: typing.ClassVar = composer_.Composed

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

    def __call__[ComposeeT](self, target: ComposeeT) -> ComposeeT:  # type: ignore[override]
        return _dispatch(self, target)
