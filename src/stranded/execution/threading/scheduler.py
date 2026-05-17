from __future__ import annotations

import abc
import dataclasses
import typing

from ..abc import scheduler


@dataclasses.dataclass(frozen=True, kw_only=True)
class Scheduler(scheduler.Scheduler, abc.ABC):
    @abc.abstractmethod
    def __call__[_Ret](self, fn: typing.Callable[[], _Ret]) -> _Ret: ...
