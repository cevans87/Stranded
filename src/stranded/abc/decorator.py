from __future__ import annotations

import abc
import dataclasses
import inspect
import types
import typing

type Instance = object
type Name = typing.Annotated[str, annotated_types.Predicate(str.isidentifier)]  # noqa


@dataclasses.dataclass(frozen=True, kw_only=True)
class Base[DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](abc.ABC):
    @property
    def param_t(self) -> type[Param[...]]:
        return Param

    @property
    def return_t(self) -> type[Return[typing.Any]]:
        return Return

    @property
    def decoratee_t(self) -> type[DecorateeT]:
        return inspect.getmodule(type(self)).Decoratee

    @property
    def receive_t(self) -> type[ReceiveT]:
        return inspect.getmodule(type(self)).Receive

    @property
    def send_t(self) -> type[SendT]:
        return inspect.getmodule(type(self)).Send

    @property
    def exit_t(self) -> type[ExitT]:
        return inspect.getmodule(type(self)).Exit

    @property
    def enter_t(self) -> type[EnterT]:
        return inspect.getmodule(type(self)).Enter

    @property
    def decorated_t(self) -> type[DecoratedT]:
        return inspect.getmodule(type(self)).Decorated

    @property
    def decorator_t(self) -> type[DecoratorT]:
        return inspect.getmodule(type(self)).Decorator


@dataclasses.dataclass(frozen=True)
class Raise:
    exc_type: type[BaseException]
    exc_val: BaseException
    exc_tb: types.TracebackType


@dataclasses.dataclass(frozen=True)
class Stop(BaseException): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Param[**ParamT]:
    args: ParamT.args = dataclasses.field(default=tuple)
    kwargs: ParamT.kwargs = dataclasses.field(default_factory=dict)


@dataclasses.dataclass(frozen=True)
class Return[RetT]:
    ret: RetT


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](typing.Protocol):
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT: ...
    def __get__(self, instance: Instance, owner: type[object] | None) -> typing.Self: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    Base[DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    decorated: DecoratedT

    def __call__[SRetT, **SParamT](
        self,
        value: Param[ParamT] | Raise | Return[SRetT] | Stop,
        /,
    ) -> Param[ParamT] | Raise | Param[typing.Concatenate[SRetT, SParamT]] | Stop:
        match value:
            case Param() as param_: return param_
            case Raise() as raise_: return raise_
            case Return() as return_: return Param(args=(return_.ret,), kwargs={})  # noqa
            case Stop() as stop_: return stop_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    Base[DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    decorated: DecoratedT

    def __call__[**RParamT](
        self,
        value: Param[ParamT] | Raise | Return[RetT] | Stop,
        /,
    ) -> Param[ParamT] | Raise | Param[typing.Concatenate[RetT, RParamT]] | Stop:
        match value:
            case Param() as param_: return param_
            case Raise() as raise_: return raise_
            case Return() as return_: return self.param_t(args=(return_.ret,), kwargs={})  # noqa
            case Stop() as stop_: return stop_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    Base[DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    enter: EnterT

    def __call__(self, value: Param[ParamT] | Raise | Return[RetT] | Stop) -> tuple[()]:
        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    Base[DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    decorated: DecoratedT

    @typing.overload
    def __call__(self, value: Param[ParamT], /) -> tuple[ExitT, DecorateeT]: ...
    @typing.overload
    def __call__(self, value: Raise | Return[RetT] | Stop, /) -> tuple[()]: ...
    def __call__(self, value: Param[ParamT] | Raise | Return[RetT] | Stop, /) -> tuple[ExitT, DecorateeT] | tuple[()]:
        match value:
            case Param(): return self.exit_t(enter=self), self.decorated.decoratee,  # type: ignore[call-arg]
            case _: return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    Base[DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    __doc__: str
    __module__: str
    __name__: str
    __qualname__: str
    __signature__: inspect.Signature
    decoratee: DecorateeT
    decorator: DecoratorT
    stack: tuple[EnterT | ExitT | ReceiveT | SendT, ...] = ()

    def __get__(self, instance: Instance, owner: type[object] | None) -> typing.Self:
        return dataclasses.replace(self, decoratee=self.decoratee.__get__(instance, owner))

    def __or__[**Param2T, Ret2T, Decoratee2T, Receive2T, Send2T, Exit2T, Enter2T, Decorated2T, Decorator2T](
        self,
        decorated: Decorated[Param2T, Ret2T, Decoratee2T, Receive2T, Send2T, Exit2T, Enter2T, Decorated2T, Decorator2T],
        /,
    ) -> Decorated[ParamT, Ret2T, Decoratee[ParamT, Ret2T], Receive2T, Send2T, Exit2T, Enter2T, Decorated2T, Decorator2T]:
        return dataclasses.replace(
            decorated,
            __doc__=f'{self.__doc__}\n\n{decorated.__doc__}',
            __module__=f'{self.__module__}, {decorated.__module__}',
            __name__=f'{self.__name__}, {decorated.__name__}',
            __qualname__=f'{self.__qualname__}, {decorated.__qualname__}',
            __signature__=inspect.Signature().replace(
                parameters=list(self.__signature__.parameters.values()),
                return_annotation=decorated.__signature__.return_annotation,
            ),
            stack=(
                decorated.receive_t(decorated=decorated),  # type: ignore[call-arg]
                self.send_t(decorated=self),  # type: ignore[call-arg]
                *self.create_context(),
                *self.stack,
            ),
        )

    def create_context(self) -> tuple[DecorateeT | ReceiveT | SendT | ExitT | EnterT | DecoratorT, ...]:
        return self.enter_t(decorated=self),  # type: ignore[call-arg]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    Base[DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    def __call__(self, decoratee: DecorateeT, /) -> DecoratedT:
        return self.decorated_t(  # type: ignore[call-arg]
            __doc__=str(decoratee.__doc__),
            __module__=str(decoratee.__module__),
            __name__=str(decoratee.__name__),
            __qualname__=str(decoratee.__qualname__),
            __signature__=inspect.signature(decoratee),
            decoratee=decoratee,
            decorator=self,
        )
