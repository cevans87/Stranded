from __future__ import annotations

import dataclasses

from .constraint import Constraint


@dataclasses.dataclass(frozen=True)
class _Base(int):
    data: int


@dataclasses.dataclass(frozen=True)
class _Int(Base): ...

    def to_positive_int() -> PositiveInt

@dataclasses.dataclass(frozen=True)
class _PositiveInt(Base): ...

    #def __post_init__(self) -> None:
    #    assert 0 < self._data


@dataclasses.dataclass(frozen=True)
class NegativeInt(Base):

    def __post_init__(self) -> None:
        assert self._data < 0


    @staticmethod
    def of_int(int_: Int) -> PositiveInt | None:
        try:
            return PositiveInt(int_.data)
        except AssertionError:
            return None

    @staticmethod
    def of_int_exc(int_: Int) -> NegativeInt:
        return NegativeInt()
