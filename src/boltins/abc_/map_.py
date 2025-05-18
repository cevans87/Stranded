from __future__ import annotations

import abc
import asyncio
import concurrent.futures
import dataclasses
import typing

from ...funktools.abc_ import decorator


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator](
    decorator.Exit[_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    params: typing.Iterator[tuple[_Param.args, _Param.kwargs]] | typing.AsyncIterator[tuple[_Param.args, _Param.kwargs]]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator](
    decorator.Enter[_Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator],
    abc.ABC,
):
    @typing.overload
    def __call__(
        self,
        params: typing.Iterable[tuple[_Param.args, _Param.kwargs]],
        /,
    ) -> tuple[typing.Iterable[_Ret]]: ...
    @typing.overload
    async def __call__(
        self,
        params: typing.AsyncIterable[tuple[_Param.args, _Param.kwargs]],
        /,
    ) -> tuple[typing.AsyncIterable[_Ret]]: ...
    @abc.abstractmethod
    def __call__(self, params, /): raise NotImplementedError()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator](
    decorator.Decorated[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator],
    abc.ABC,
): ...


class Decorator[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated](
    decorator.Decorator[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
):
    loop: asyncio.AbstractEventLoop = dataclasses.field(
        default_factory=asyncio.get_event_loop,
    )
    pool: concurrent.futures.ThreadPoolExecutor = dataclasses.field(
        default_factory=concurrent.futures.ThreadPoolExecutor,
    )

