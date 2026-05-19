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
class Base[_Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](abc.ABC):
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
    def connect_t(self) -> type[_Connect]:
        return inspect.getmodule(type(self)).Connect

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
class OperationState[
    **_SParam, _SRet, _SDecoratee, _SConnect, _SExit, _SEnter, _SDecorated, _SDecorator,
    **_RParam, _RRet, _RDecoratee, _RConnect, _RExit, _REnter, _RDecorated, _RDecorator,
](
    Base[_SDecoratee, _SConnect, _SExit, _SEnter, _SDecorated, _SDecorator],
    abc.ABC,
):
    sender: _SDecorator
    receiver: _RDecorator

    def __call__(self, s_ret: _SRet, *s_args: _SParam.args, **s_kwargs: _SParam.kwargs) -> Param[_RParam]:
        # TODO
        ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**_SParam, _SRet, _SDecoratee, _SConnect, _SExit, _SEnter, _SDecorated, _SDecorator](
    Base[_SDecoratee, _SConnect, _SExit, _SEnter, _SDecorated, _SDecorator],
    abc.ABC,
):
    sender: Decorator[_SParam, _SRet, _SDecoratee, _SConnect, _SExit, _SEnter, _SDecorated, _SDecorator]

    def __call__[**_RParam, _RRet, _RDecoratee, _RConnect, _RExit, _REnter, _RDecorated, _RDecorator](
        self,
        sender: Decorator[
            _SParam,
            _SRet,
            _SDecoratee,
            _SConnect,
            _SExit,
            _SEnter,
            _SDecorated,
            _SDecorator,
        ],
        receiver: Decorator[_RParam, _RRet, _RDecoratee, _RConnect, _RExit, _REnter, _RDecorated, _RDecorator],
    ) -> OperationState[
        _SParam, _SRet, _SDecoratee, _SConnect, _SExit, _SEnter, _SDecorated, _SDecorator,
        _RParam, _RRet, _RDecoratee, _RConnect, _RExit, _REnter, _RDecorated, _RDecorator,
    ]:
        return OperationState(sender=sender, receiver=receiver)




@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    Base[_Decoratee, _Connect, _Enter, _Exit, _Decorated, _Decorator],
    abc.ABC,
):
    enter: _Enter

    def __call__(self, result: Raise | _Ret) -> tuple[()]:
        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    Base[_Decoratee, _Connect, _Decorator, _Decorated, _Enter, _Exit],
    abc.ABC,
):
    decorated: _Decorated

    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Exit, _Decoratee]:
        return self.exit_t(enter=self), self.decorated.decoratee,


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    Base[_Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    __doc__: str
    __module__: str
    __name__: str
    __qualname__: str
    __signature__: inspect.Signature
    decoratee: _Decoratee
    decorator: _Decorator
    stack: tuple[OperationState | Decorated, ...] = ()

    def __get__(self, instance: Instance, owner) -> typing.Self:
        return dataclasses.replace(self, decoratee=self.decoratee.__get__(instance, owner))

    def __or__[**_Param2, _Ret2, _Decoratee2, _Connect2, _Exit2, _Enter2, _Decorated2, _Decorator2](
        self,
        receiver: Decorated[_Param2, _Ret2, _Decoratee2, _Connect2, _Exit2, _Enter2, _Decorated2, _Decorator2],
        /,
    ) -> Decorated[_Param, _Ret2, Decoratee[_Param, _Ret2], _Connect2, _Exit2, _Enter2, _Decorated2, _Decorator2]:
        return dataclasses.replace(
            receiver,
            __doc__=f'{self.__doc__}\n\n{receiver.__doc__}',
            __module__ = f'{self.__module__}, {receiver.__module__}',
            __name__ = f'{self.__name__}, {receiver.__name__}',
            __qualname__ = f'{self.__qualname__}, {receiver.__qualname__}',
            __signature__ = inspect.Signature().replace(
                parameters = self.__signature__.parameters,
                return_annotation = receiver.__signature__.return_annotation,
            ),
            stack=(self.connect_t()(sender=self, reciever=receiver), self, *self.stack),
        )



    def create_context(self) -> tuple[_Decoratee | _Connect | _Exit | _Enter | _Decorator, ...]:
        return self.enter_t(decorated=self),


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    Base[_Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
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
