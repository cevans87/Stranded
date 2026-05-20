from __future__ import annotations

import abc
import dataclasses
import inspect
import types
import typing

type Instance = object
type Name = typing.Annotated[str, annotated_types.Predicate(str.isidentifier)]  # noqa


class Exception(Exception): ...  # noqa


@dataclasses.dataclass(frozen=True)
class Raise:
    exc_type: type[BaseException]
    exc_val: BaseException
    exc_tb: types.TracebackType


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](typing.Protocol):
    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> _Ret: ...
    def __get__(self, instance: Instance, owner) -> typing.Self: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Base[_Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator](abc.ABC):
    @property
    def decoratee_t(self) -> type[_Decoratee]:
        return inspect.getmodule(type(self)).Decoratee

    @property
    def param_t(self) -> type[Param]:
        return inspect.getmodule(type(self)).Param

    @property
    def receive_t(self) -> type[_Receive]:
        return inspect.getmodule(type(self)).Receive

    @property
    def send_t(self) -> type[_Send]:
        return inspect.getmodule(type(self)).Send

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
    def decorator_t(self) -> type[_Decorator]:
        return inspect.getmodule(type(self)).Decorator



@dataclasses.dataclass(frozen=True, kw_only=True)
class Param[**_Param]:
    args: _Param.args = dataclasses.field(default=tuple)
    kwargs: _Param.kwargs = dataclasses.field(default_factory=dict)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator](
    Base[_Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    decorated: _Decorated

    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> Param[_Param]:
        return self.param_t(args=args, kwargs=kwargs)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator](
    Base[_Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    decorated: _Decorated

    def __call__(self, result: Raise | _Ret) -> Param[_Param]:
        return self.param_t(args=(result,), kwargs={})


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator](
    Base[_Decoratee, _Receive, _Send, _Enter, _Exit, _Decorated, _Decorator],
    abc.ABC,
):
    enter: _Enter

    def __call__(self, result: Raise | _Ret) -> tuple[()]:
        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator](
    Base[_Decoratee, _Receive, _Send, _Decorator, _Decorated, _Enter, _Exit],
    abc.ABC,
):
    decorated: _Decorated

    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Exit, _Decoratee]:
        return self.exit_t(enter=self), self.decorated.decoratee,


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator](
    Base[_Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    __doc__: str
    __module__: str
    __name__: str
    __qualname__: str
    __signature__: inspect.Signature
    decoratee: _Decoratee
    decorator: _Decorator
    stack: tuple[Decorated | Receive | Send, ...] = ()

    def __get__(self, instance: Instance, owner) -> typing.Self:
        return dataclasses.replace(self, decoratee=self.decoratee.__get__(instance, owner))

    def __or__[**_Param2, _Ret2, _Decoratee2, _Receive2, _Send2, _Exit2, _Enter2, _Decorated2, _Decorator2](
        self,
        decorated: Decorated[_Param2, _Ret2, _Decoratee2, _Receive2, _Send2, _Exit2, _Enter2, _Decorated2, _Decorator2],
        /,
    ) -> Decorated[_Param, _Ret2, Decoratee[_Param, _Ret2], _Receive2, _Send2, _Exit2, _Enter2, _Decorated2, _Decorator2]:
        return dataclasses.replace(
            decorated,
            __doc__=f'{self.__doc__}\n\n{decorated.__doc__}',
            __module__ = f'{self.__module__}, {decorated.__module__}',
            __name__ = f'{self.__name__}, {decorated.__name__}',
            __qualname__ = f'{self.__qualname__}, {decorated.__qualname__}',
            __signature__ = inspect.Signature().replace(
                parameters = list(self.__signature__.parameters.values()),
                return_annotation = decorated.__signature__.return_annotation,
            ),
            stack=(decorated.receive_t(decorated=decorated), self.send_t(decorated=self), self, *self.stack),
        )



    def create_context(self) -> tuple[_Decoratee | _Receive | _Send | _Exit | _Enter | _Decorator, ...]:
        return self.enter_t(decorated=self),


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator](
    Base[_Decoratee, _Receive, _Send, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
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