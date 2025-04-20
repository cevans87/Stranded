from __future__ import annotations

import abc
import asyncio
import dataclasses
import typing
from inspect import iscoroutinefunction

#from ..abc_ import iter_ as abc_iter_
#from . import filter_ as asyncio_filter_


@dataclasses.dataclass(frozen=True)
class T[_V]:
    _vs: typing.AsyncIterable[_V]

    def __aiter__(self) -> typing.AsyncIterable[_V]:
        return self._vs

    @typing.overload
    def filter(self, f: typing.Callable[[_V], typing.Awaitable[bool]], /) -> typing.Self: ...
    @typing.overload
    def filter(self, f: typing.Callable[[_V], bool], /) -> typing.Self: ...
    @typing.overload
    def filter(self, f: None, /) -> typing.Self: ...
    def filter(self, f=None, /):
        async def apply(_f):
            match _f:
                case None:
                    async for v in self._vs:
                        if v:
                            yield v
                case _ if iscoroutinefunction(_f):
                    async for v in self._vs:
                        if await _f(v):
                            yield v
                case _:
                    async for v in self._vs:
                        if _f(v):
                            yield v

        return dataclasses.replace(self, _vs=apply(f))

    @typing.overload
    def map[_U](self, f: typing.Callable[[_V], typing.Awaitable[_U]], /) -> T[_U]: ...
    @typing.overload
    def map[_U](self, f: typing.Callable[[_V], _U], /) -> T[_U]: ...
    def map[_U](self, f, /):
        async def apply(_f) -> typing.AsyncIterator[_U]:
            match _f:
                case _f if iscoroutinefunction(_f):
                    async for v in self._vs:
                        yield await _f(v)
                case _f:
                    async for v in self._vs:
                        yield _f(v)

        return T(apply(f))

    @typing.overload
    async def reduce(self, v: _V, f: typing.Callable[[_V, _V], typing.Awaitable[_V]], /) -> _V: ...
    @typing.overload
    async def reduce(self, v: _V, f: typing.Callable[[_V, _V], _V], /) -> _V: ...
    async def reduce(self, v: _V, f, /):
        match iscoroutinefunction(f):
            case True:
                async for _v in self._vs:
                    v = await f(v, _v)
            case False:
                async for _v in self._vs:
                    v = f(v, _v)
        return v
