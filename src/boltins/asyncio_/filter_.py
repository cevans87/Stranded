from __future__ import annotations

import abc
import dataclasses
import typing
from inspect import iscoroutinefunction


@dataclasses.dataclass(frozen=True)
class T[_Value]:
    _f: typing.Callable[[_Value], bool] | typing.Callable[[_Value], typing.Awaitable[bool]] | None
    _values: typing.AsyncIterable[_Value]

    async def __aiter__(self) -> typing.AsyncIterable[_Value]:
        match self._f:
            case None: yield (value async for value in self._values if value)
            case f if iscoroutinefunction(f): yield (value async for value in self._values if await f(value))
            case f: yield (value async for value in self._values if f(value))

    def __await__(self):
        return self.__aiter__()


@dataclasses.dataclass(frozen=True)
class Mixin[_Value](abc.ABC):
    type Filter = T[_Value]

    @abc.abstractmethod
    @property
    def _values(self) -> typing.AsyncIterable[_Value]: raise NotImplemented()

    @typing.overload
    async def filter(self, f: typing.Callable[[_Value], typing.Awaitable[bool]], /) -> Filter: ...
    @typing.overload
    async def filter(self, f: typing.Callable[[_Value], bool], /) -> Filter: ...
    @typing.overload
    async def filter(self, f: None, /) -> Filter: ...
    async def filter(self, f=None, /): return await T(f, self._values)
