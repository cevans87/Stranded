from __future__ import annotations

import abc
import dataclasses
import typing

from . import composer_
from ..builtins import exception_


class Exception(exception_.Exception): ...  # noqa


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer_.Exit[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheduler[**ParamT, RetT](composer_.Composer[ParamT, RetT], abc.ABC):
    # A Scheduler is its own ergonomic composer: the wrapped Composee keeps the
    # callee's call signature. The composition machinery still receives the real
    # Composed produced by Composer.__call__.
    def __call__[ComposeeT](self, composee: ComposeeT, /) -> ComposeeT:  # type: ignore[override]
        return typing.cast(
            'ComposeeT',
            super().__call__(typing.cast('composer_.Composee[typing.Any, typing.Any]', composee)),
        )

    @abc.abstractmethod
    def submit_sync(
        self,
        fn: typing.Callable[..., typing.Any],
        args: tuple[typing.Any, ...],
        kwargs: dict[str, typing.Any],
    ) -> typing.Any: ...

    @abc.abstractmethod
    async def submit_async(
        self,
        fn: typing.Callable[..., typing.Any],
        args: tuple[typing.Any, ...],
        kwargs: dict[str, typing.Any],
    ) -> typing.Any: ...
