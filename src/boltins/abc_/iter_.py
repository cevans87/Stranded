from __future__ import annotations

import abc
import typing

class T[_Value](typing.Iterable[_T], abc.ABC):

    @typing.overload
    async def filter(self, *, f: typing.Callable[[_T], typing.Awaitable[_T | None]]) -> T[_T]: ...

    @typing.overload
    def filter(self, *, f: typing.Callable[[_T], _T | None]) -> T[_T]: ...

    @abc.abstractmethod
    def filter(self, *, f): raise NotImplementedError()

    @abc.abstractmethod
    async def fold[_U](self, _u: _U, /, f: typing.Callable[[_T, _U], typing.Awaitable[_U]]) -> _U: ...

    @abc.abstractmethod
    async def map[_U](self, f: typing.Callable[[_T], typing.Awaitable[_U]]) -> abc_iterable.T[_U]: ...

    @abc.abstractmethod
    def map[_U](self, f: typing.Callable[[_T], typing.Awaitable[_U]]) -> abc_iterable.T[_U]: ...

    #@typing.overload
    #async def reduce(self, f: typing.Callable[[_T, _T], typing.Awaitable[_T]]) -> _T: ...

    #@typing.overload
    #def reduce(self, v: _Value, f: typing.Callable[[_T, _T], _T]) -> _T: ...

    #@abc.abstractmethod
    #def reduce(self, f): raise NotImplementedError()
