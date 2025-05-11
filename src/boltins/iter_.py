from __future__ import annotations

import abc
import dataclasses
import importlib
import inspect
import typing

from .abc_ import iter_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Iter(iter_.Iter, abc.ABC):

    @typing.overload
    def __call__(self, vs: typing.AsyncIterable) -> iter_.Iter: ...
    @typing.overload
    def __call__(self, vs: typing.Iterable) -> iter_.Iter: ...
    def __call__(self, vs): return importlib.import_module(
            name='.'.join(
                (name_parts := self.__module__.split('.')).insert(
                    -1,
                    'asyncio_' if inspect.isasyncgen(vs) else 'threading_'
                ) or name_parts
            )
        ).T(vs)
