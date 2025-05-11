from __future__ import annotations

import abc
import typing

from ...funktools.abc_ import decorator as abc_decorator

class Iter[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Filter, _Map, _Reduce](
    abc_decorator.Decorator[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
):

    @typing.overload
    def filter(self, f: typing.Callable[[_V], typing.Awaitable[bool]], /) -> typing.Self: ...
    @typing.overload
    def filter(self, f: typing.Callable[[_V], bool], /) -> typing.Self: ...
    @abc.abstractmethod
    def filter(self, f: None, /) -> typing.Self: raise NotImplemented()

    @typing.overload
    def map[_Ret2](self, f: typing.Callable[[_Ret], typing.Awaitable[_Ret2]], /) -> Iter[_Ret2]: ...
    @typing.overload
    def map[_Ret2](self, f: typing.Callable[[_Ret], _Ret2], /) -> Iter[_Ret2]: ...
    @abc.abstractmethod
    def map(self, f): raise NotImplemented()

    @typing.overload
    def reduce[_Ret2](self, f: typing.Callable[[_Ret], typing.Awaitable[_Ret2]], /) -> _Reduce: ...
    @typing.overload
    def reduce[_Ret2](self, f: typing.Callable[[_Ret], _Ret2], /) -> _Reduce: ...
    @abc.abstractmethod
    def reduce(self, f, /): raise NotImplemented()
