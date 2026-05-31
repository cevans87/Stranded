from __future__ import annotations

import abc
import dataclasses
import typing

from . import decorator
from ..builtins import exception_


class Exception(exception_.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](decorator.Exit[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](decorator.Enter[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](decorator.Decorated[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheduler[**ParamT, RetT](decorator.Decorator[ParamT, RetT], abc.ABC):
    # A Scheduler is its own ergonomic decorator: the wrapped Decoratee keeps the
    # callee's call signature. The composition machinery still receives the real
    # Decorated produced by Decorator.__call__.
    def __call__[DecorateeT](self, decoratee: DecorateeT, /) -> DecorateeT:  # type: ignore[override]
        return typing.cast(
            'DecorateeT',
            super().__call__(typing.cast('decorator.Decoratee[typing.Any, typing.Any]', decoratee)),
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
