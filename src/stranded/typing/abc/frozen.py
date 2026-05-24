import abc
import typing


class Frozen[TT: typing.Hashable](abc.ABC):

    @abc.abstractmethod
    def __hash__(self) -> int: raise NotImplemented()

    @typing.final
    def __setattr__(self, key: str, value: object) -> None: raise RuntimeError(f'Instance is frozen. {self=!r}')

    @typing.final
    def __setitem__(self, key: object, value: object) -> None: raise RuntimeError(f'Instance is frozen. {self=!r}')