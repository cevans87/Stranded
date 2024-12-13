import typing

from . import constraint

class Int[C: constraint.Constraint]:
    _constraint=lambda _value: True

    def __get__(self, obj, objtype=None) -> typing.Self:
        return self._value

    def __set__(self, obj, value: int) -> None:
        self._value = value