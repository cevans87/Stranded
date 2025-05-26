from __future__ import annotations

import asyncio
import dataclasses
import typing

from ..abc_ import map_
from . import executor

type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Decorator[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    executor.Decoratee[_Param, _Ret],
    map_.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret](
    executor.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    map_.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret](
    executor.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    map_.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret](
    executor.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    map_.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
):
    async def __call__(
        self,
        params: typing.AsyncIterable[tuple[_Param.args, _Param.kwargs]],
        /,
    ) -> typing.AsyncIterable[_Ret]:
        q = asyncio.LifoQueue()
        n = 0
        condition = asyncio.Condition()

        async def putter(*args: _Param.args, **kwargs: _Param.kwargs) -> None:
            nonlocal n, self
            try:
                _ret = await self.decoratee(*args, **kwargs)
            except Exception as _e:
                await q.put(_e)
            else:
                await q.put(_ret)

            async with condition:
                n -= 1
                if n ==0:
                    condition.notify()

        async def submitter() -> None:
            nonlocal n
            async for (args, kwargs) in params:
                async with condition:
                    n += 1
                asyncio.ensure_future(putter(*args, **kwargs), loop=self.decorator.loop)

            async with condition:
                await condition.wait_for(lambda: n == 0)

            q.shutdown()

        asyncio.ensure_future(submitter(), loop=self.decorator.loop)

        while True:
            try:
                result = await q.get()
            except asyncio.QueueShutDown:
                break

            match result:
                case Exception() as e:
                    raise e
                case ret:
                    yield ret


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret](
    executor.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
    ],
    map_.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
    ],
): ...
