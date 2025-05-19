import dataclasses
import inspect
import typing

from .abc_ import map_


@typing.runtime_checkable
class AsyncioDecoratee[**_Param, _Ret](map_.Decoratee[_Param, _Ret], typing.Protocol):
    async def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> _Ret: ...


class AsyncioDecorated[**_Param, _Ret](
    AsyncioDecoratee[_Param, _Ret],
    typing.Protocol,
):
    @typing.overload
    async def __call__(
        self,
        params: typing.Iterable[tuple[_Param.args, _Param.kwargs]]
    ) -> typing.AsyncIterable[_Ret]: ...
    @typing.overload
    async def __call__(
        self,
        params: typing.AsyncIterable[tuple[_Param.args, _Param.kwargs]]
    ) -> typing.AsyncIterable[_Ret]: ...
    async def __call__(self, params): ...


@typing.runtime_checkable
class ThreadingDecoratee[**_Param, _Ret](map_.Decoratee[_Param, _Ret], typing.Protocol):
    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> _Ret: ...


class ThreadingDecorated[**_Param, _Ret](
    ThreadingDecoratee[_Param, _Ret],
    typing.Protocol,
):
    @typing.overload
    def __call__(
        self,
        params: typing.Iterable[tuple[_Param.args, _Param.kwargs]]
    ) -> typing.AsyncIterable[_Ret]: ...
    @typing.overload
    def __call__(
        self,
        params: typing.AsyncIterable[tuple[_Param.args, _Param.kwargs]]
    ) -> typing.AsyncIterable[_Ret]: ...
    def __call__(self, params): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Map(map_.Decorator):
    @typing.overload
    def __call__[**_Param, _Ret, _Decoratee: AsyncioDecoratee[_Param, _Ret]](
        self,
        decoratee: AsyncioDecoratee[_Param, _Ret],
        /,
    ) -> AsyncioDecorated[_Param, _Ret]: ...
    @typing.overload
    def __call__[**_Param, _Ret, _Decoratee: ThreadingDecoratee[_Param, _Ret]](
        self,
        decoratee: _Decoratee,
        /,
    ) -> ThreadingDecorated[_Param, _Ret]: ...
    def __call__(self, decoratee, /):
        match decoratee:
            case AsyncioDecoratee():
                from .asyncio_.map_ import Decorator
                return Decorator(loop=self.loop, pool=self.pool)(decoratee)
            case ThreadingDecoratee():
                from .threading_.map_ import Decorator
                return Decorator(loop=self.loop, pool=self.pool)(decoratee)
        match inspect.iscoroutinefunction(decoratee):
            case True:
                from .asyncio_.map_ import Decorator
                return Decorator(loop=self.loop, pool=self.pool)(decoratee)
            case False:
                from .threading_.map_ import Decorator
                return Decorator(loop=self.loop, pool=self.pool)(decoratee)

