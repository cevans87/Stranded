from __future__ import annotations

import dataclasses
import threading
import typing

from funktools.threading_ import decorator
from ..abc_ import reduce


type _Decoratee[**_Param, _Ret] = Decoratee[_Param, _Ret]
type _Exit[**_Param, _Ret] = Exit[_Param, _Ret]
type _Enter[**_Param, _Ret] = Enter[_Param, _Ret]
type _Decorated[**_Param, _Ret] = Decorated[_Param, _Ret]
type _Decorator[**_Param, _Ret] = Decorator[_Param, _Ret]


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    reduce.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret](
    decorator.Exit[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    reduce.Exit[
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
    decorator.Enter[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Decorated[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    reduce.Enter[
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
    decorator.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
    reduce.Decorated[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorator[_Param, _Ret],
    ],
):
    _busy: typing.ClassVar[object] = object()

    @typing.override
    def __call__(
        self,
        params: typing.Iterable[tuple[_Param.args, _Param.kwargs]],
        /,
    ) -> _Ret:
        accum = self.decorator.init
        n = 0
        condition = threading.Condition()

        def reducer(right: _Ret) -> None:
            nonlocal accum, n
            while True:
                with condition:
                    if accum is not self._busy:
                        left, accum = accum, self._busy
                    else:
                        accum = right
                        n -= 1
                        if n == 0:
                            condition.notify()
                        break

                right = self.decoratee(left, right)

        for (args, kwargs) in params:
            with condition:
                n += 1
            self.decorator.pool.submit(reducer, *args, **kwargs)

        with condition:
            condition.wait_for(lambda: n == 0)

        return accum


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret](
    decorator.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
    ],
    reduce.Decorator[
        _Param,
        _Ret,
        _Decoratee[_Param, _Ret],
        _Exit[_Param, _Ret],
        _Enter[_Param, _Ret],
        _Decorated[_Param, _Ret],
    ],
): ...
