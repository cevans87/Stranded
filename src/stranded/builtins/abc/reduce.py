from __future__ import annotations

import abc
import dataclasses
import typing

from . import executor


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    executor.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator](
    executor.Exit[_Param, _Ret, _Decoratee, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator](
    executor.Enter[_Param, _Ret, _Decoratee, _Exit, _Decorated, _Decorator],
    abc.ABC,
):
    @typing.overload
    def __call__(
        self,
        params: typing.Iterable[tuple[_Param.args, _Param.kwargs]],
        /,
    ) -> _Ret: ...
    @typing.overload
    async def __call__(
        self,
        params: typing.AsyncIterable[tuple[_Param.args, _Param.kwargs]],
        /,
    ) -> _Ret: ...
    @abc.abstractmethod
    def __call__(self, rets, /): raise NotImplementedError()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator](
    executor.Decorated[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorator],
    abc.ABC,
):
    class _Busy: pass
    _busy: typing.ClassVar[_Busy] = _Busy()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated](
    executor.Decorator[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
):
    init: _Ret

