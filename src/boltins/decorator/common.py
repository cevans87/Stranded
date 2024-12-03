from __future__ import annotations

import abc
import dataclasses
import inspect
import types
import typing


class Exception(Exception): ...  # noqa

@typing.runtime_checkable
class Decoratee[** Param, Ret](typing.Protocol):
    def __get__(self, instance: Instance, owner) -> typing.Self: ...


type Instance = object
type Name = typing.Annotated[str, annotated_types.Predicate(str.isidentifier)]  # noqa


@dataclasses.dataclass(frozen=True)
class Raise:
    exc_type: type[BaseException]
    exc_val: BaseException
    exc_tb: types.TracebackType


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[_Enter, _Ret](abc.ABC):
    enter: _Enter

    def __call__(self, result: Raise | _Ret) -> ():
        return tuple()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[_Decoratee, _Exit, _Decorated, **_Param](abc.ABC):
    decorated: _Decorated

    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Exit, _Decoratee]:
        return self.decorated.decorator.exit_t(enter=self), self.decorated.decoratee,


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[_Decoratee, _Exit, _Enter, _Decorator](abc.ABC):
    __doc__: str
    __module__: str
    __name__: str
    __qualname__: str
    __signature__: inspect.Signature
    decoratee: _Decoratee
    decorator: _Decorator

    def __get__(self, instance: Instance, owner) -> typing.Self:
        return dataclasses.replace(self, decoratee=self.decoratee.__get__(instance, owner))


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[_Decoratee, _Exit, _Enter, _Decorated](abc.ABC):

    @property
    def decoratee_t(self) -> type[_Decoratee]:
        return inspect.getmodule(type(self)).Decoratee

    @property
    def exit_t(self) -> type[_Exit]:
        return inspect.getmodule(type(self)).Exit

    @property
    def enter_t(self) -> type[_Enter]:
        return inspect.getmodule(type(self)).Enter

    @property
    def decorated_t(self) -> type[_Decorated]:
        return inspect.getmodule(type(self)).Decorated

    @property
    def decorator_t(self) -> type[typing.Self]:
        return inspect.getmodule(type(self)).Decorator

    def __call__(self, decoratee: _Decoratee, /) -> _Decorated:
        return self.decorated_t(
            __doc__=str(decoratee.__doc__),
            __module__=str(decoratee.__module__),
            __name__=str(decoratee.__name__),
            __qualname__=str(decoratee.__qualname__),
            __signature__=inspect.signature(decoratee),
            decoratee=decoratee,
            decorator=self,
        )


