import abc
import typing


class Frozen[_T: typing.Hashable](abc.ABC):

    @abc.abstractmethod
    def __hash__(self) -> int: raise NotImplemented()

    @typing.final
    def __setattr__(self, key, value): raise RuntimeError(f'Instance is frozen. {self=!r}')

    @typing.final
    def __setitem__(self, key, value): raise RuntimeError(f'Instance is frozen. {self=!r}')