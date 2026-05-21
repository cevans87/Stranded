from __future__ import annotations

import abc
import typing

from . import iterable as abc_iterable

class T[TT, VT](typing.Iterable[TT], abc.ABC):

    @typing.overload
    async def filter(self, *, f: typing.Callable[[TT], typing.Awaitable[TT | None]]) -> T[TT]: ...

    @typing.overload
    def filter(self, *, f: typing.Callable[[TT], TT | None]) -> T[TT]: ...

    @abc.abstractmethod
    def filter(self, *, f): raise NotImplementedError()

    @abc.abstractmethod
    async def fold[UT](self, _u: UT, /, f: typing.Callable[[TT, UT], typing.Awaitable[UT]]) -> UT: ...

    @abc.abstractmethod
    async def map[UT](self, f: typing.Callable[[TT], typing.Awaitable[UT]]) -> abc_iterable.T[UT]: ...

    @abc.abstractmethod
    def map[UT](self, f: typing.Callable[[TT], typing.Awaitable[UT]]) -> abc_iterable.T[UT]: ...

    @typing.overload
    async def reduce(self, f: typing.Callable[[TT, TT], typing.Awaitable[TT]]) -> TT: ...

    @typing.overload
    def reduce(self, f: typing.Callable[[TT, TT], TT]) -> TT: ...

    @abc.abstractmethod
    def reduce(self, f): raise NotImplementedError()
