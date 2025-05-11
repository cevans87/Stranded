from __future__ import annotations

import asyncio
import dataclasses
import inspect
import typing

from ..abc_ import iter_ as abc_iter_


@dataclasses.dataclass(frozen=True)
class Iter[_U, _V](abc_iter_.Iter[_V]):

    _vs: typing.Iterable[_V]

    def __aiter__(self) -> typing.Iterable[_V]:
        return self._vs

    @typing.overload
    @typing.override
    def filter(self, f: typing.Callable[[_V], typing.Awaitable[bool]], /) -> typing.Self: ...
    @typing.overload
    @typing.override
    def filter(self, f: typing.Callable[[_V], bool], /) -> typing.Self: ...
    @typing.overload
    @typing.override
    def filter(self, f: None, /) -> typing.Self: ...
    @typing.override
    def filter(self, f=None, /):
        def apply(_f) -> typing.Iterable[_V]:
            match inspect.iscoroutinefunction(_f):
                case True:
                    for v in self._vs:
                        if asyncio.run(_f(v)):
                            yield v
                case False:
                    for v in self._vs:
                        if _f(v):
                            yield v

        return dataclasses.replace(self, _vs=apply(f))

    @typing.overload
    @typing.override
    def map[_W](self, f: typing.Callable[[_V], typing.Awaitable[_W]], /) -> Iter[_W]: ...
    @typing.overload
    @typing.override
    def map[_W](self, f: typing.Callable[[_V], _W], /) -> Iter[_W]: ...
    @typing.override
    def map[_W](self, f, /):
        def apply(_f) -> typing.Iterable[_W]:
            match inspect.iscoroutinefunction(_f):
                case True:
                    for v in self._vs:
                        yield asyncio.run(_f(v))
                case False:
                    for v in self._vs:
                        yield _f(v)

        return Iter(apply(f))

    @typing.overload
    @typing.override
    def reduce(self, v: _V, f: typing.Callable[[_V, _V], typing.Awaitable[_V]], /) -> _V: ...
    @typing.overload
    @typing.override
    def reduce(self, v: _V, f: typing.Callable[[_V, _V], _V], /) -> _V: ...
    @typing.override
    def reduce(self, v, f, /):
        # TODO allow taking first value as v.
        match inspect.iscoroutinefunction(f):
            case True:
                for _v in self._vs:
                    v = asyncio.run(f(v, _v))
            case False:
                for _v in self._vs:
                    v = f(v, _v)
        return v
