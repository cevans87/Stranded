import abc
import typing


class T[_T](typing.Iterable[_T], abc.ABC):
    pass
