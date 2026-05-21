import abc
import typing


class T[TT](typing.Iterable[TT], abc.ABC):
    pass
