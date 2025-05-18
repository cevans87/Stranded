import dataclasses
import inspect
import typing

from .abc_ import map_


class AsyncioDecoratee[**_Param, _Ret](map_.Decoratee[_Param, _Ret], typing.Protocol):
    async def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> _Ret: ...


class AsyncioDecorated[_Param, _Ret](
    map_.Decorated[_Param, _Ret],
    AsyncioDecoratee[_Param, _Ret],
    typing.Protocol,
): ...


class ThreadingDecoratee[**_Param, _Ret](map_.Decoratee[_Param, _Ret], typing.Protocol):
    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> _Ret: ...


class ThreadingDecorated[_Param, _Ret](
    map_.Decorated[_Param, _Ret],
    ThreadingDecoratee[_Param, _Ret],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Map(map_.Decorator):
    @typing.overload
    def __call__[**_Param, _Ret](
        self,
        decoratee: AsyncioDecoratee[_Param, _Ret],
        /,
    ) -> AsyncioDecorated[_Param, _Ret]: ...
    @typing.overload
    def __call__[**_Param, _Ret](
        self,
        decoratee: ThreadingDecoratee[_Param, _Ret],
        /,
    ) -> ThreadingDecorated[_Param, _Ret]: ...
    def __call__(self, decoratee, /):
        match inspect.iscoroutinefunction(decoratee):
            case True:
                from .asyncio_.map_ import Decorator
                return Decorator(loop=self.loop, pool=self.pool)(decoratee)
            case False:
                from .threading_.map_ import Decorator
                return Decorator(loop=self.loop, pool=self.pool)(decoratee)

