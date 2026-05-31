from __future__ import annotations

import abc
import dataclasses
import inspect
import types
import typing

type Instance = object

type ValueT[**ParamT_, RetT_] = Param[ParamT_] | Raise | Return[RetT_] | Stop
type StackT = tuple[
    ValueT[typing.Any, typing.Any]
    | Decoratee[typing.Any, typing.Any]
    | Connect[typing.Any, typing.Any]
    | Exit[typing.Any, typing.Any]
    | Enter[typing.Any, typing.Any]
    | Decorated[typing.Any, typing.Any],
    ...,
]


@dataclasses.dataclass(frozen=True)
class Raise:
    exc_type: type[BaseException]
    exc_val: BaseException
    exc_tb: types.TracebackType | None


@dataclasses.dataclass(frozen=True)
class Stop(BaseException): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Param[**ParamT]:
    args: ParamT.args
    kwargs: ParamT.kwargs


@dataclasses.dataclass(frozen=True)
class Return[RetT]:
    ret: RetT


class Decoratee[**ParamT, RetT](typing.Protocol):
    __doc__: str
    __module__: str
    __name__: str
    __qualname__: str
    __signature__: inspect.Signature
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT: ...
    def __get__(self, instance: Instance, owner: type[object] | None) -> typing.Self: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](abc.ABC):
    decorator: Decorator[ParamT, RetT]
    stack: StackT

    def __call__(self, value: ValueT[ParamT, RetT], /) -> StackT:
        match value:
            case Param() as param_: return *self.stack, param_
            case Raise() as raise_: return raise_,
            case Return() as return_: return *self.stack, Param(args=(return_.ret,), kwargs={}),
            case Stop() as stop_: return stop_,


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](abc.ABC):
    enter: Enter[ParamT, RetT]

    @property
    def decorator(self) -> Decorator[typing.Any, typing.Any]: return self.enter.decorator
    @property
    def decoratee_t(self) -> type[Decoratee[typing.Any, typing.Any]]: return self.decorator.decoratee_t
    @property
    def exit_t(self) -> type[Exit[typing.Any, typing.Any]]: return self.decorator.exit_t
    @property
    def enter_t(self) -> type[Enter[typing.Any, typing.Any]]: return self.decorator.enter_t
    @property
    def decorated_t(self) -> type[Decorated[typing.Any, typing.Any]]: return self.decorator.decorated_t

    def __call__(self, value: ValueT[ParamT, RetT], /) -> StackT:
        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](abc.ABC):
    decorator: Decorator[ParamT, RetT]
    decoratee: Decoratee[ParamT, RetT]

    @property
    def decoratee_t(self) -> type[Decoratee[typing.Any, typing.Any]]: return self.decorator.decoratee_t
    @property
    def exit_t(self) -> type[Exit[typing.Any, typing.Any]]: return self.decorator.exit_t
    @property
    def enter_t(self) -> type[Enter[typing.Any, typing.Any]]: return self.decorator.enter_t
    @property
    def decorated_t(self) -> type[Decorated[typing.Any, typing.Any]]: return self.decorator.decorated_t

    def __call__(self, value: ValueT[ParamT, RetT], /) -> StackT:
        match value:
            case Param(): return self.exit_t(enter=self), self.decoratee,
            case _: return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](abc.ABC):
    __doc__: str
    __module__: str
    __name__: str
    __qualname__: str
    __signature__: inspect.Signature
    stack: StackT
    decorator: Decorator[ParamT, RetT]

    @property
    def decoratee_t(self) -> type[Decoratee[typing.Any, typing.Any]]: return self.decorator.decoratee_t
    @property
    def connect_t(self) -> type[Connect[typing.Any, typing.Any]]: return self.decorator.connect_t
    @property
    def exit_t(self) -> type[Exit[typing.Any, typing.Any]]: return self.decorator.exit_t
    @property
    def enter_t(self) -> type[Enter[typing.Any, typing.Any]]: return self.decorator.enter_t
    @property
    def decorated_t(self) -> type[Decorated[typing.Any, typing.Any]]: return self.decorator.decorated_t

    @property
    def decoratee(self) -> Decoratee[ParamT, RetT]:
        # The decoratee lives on the Enter at the base of the stack. Sub-domain code that
        # used to read self.decorated.decoratee now reads it through this accessor.
        match self.stack:
            case [*_, Enter() as enter_]: return enter_.decoratee
        assert False, "unreachable"

    def __get__(self, instance: Instance, owner: type[object] | None) -> typing.Self:
        match self.stack:
            case [*_, Enter() as enter_]:
                return dataclasses.replace(
                    self,
                    stack=(
                        *self.stack[:-1],
                        dataclasses.replace(enter_, decoratee=enter_.decoratee.__get__(instance, owner)),
                    )
                )
        assert False, "unreachable"

    def __or__[**OtherParamT, OtherRetT](
        self,
        other_decorated: Decorated[OtherParamT, OtherRetT],
        /,
    ) -> Decorated[ParamT, OtherRetT]:
        return dataclasses.replace(
            self, stack=(self.connect_t(decorator=self.decorator, stack=other_decorated.stack), *self.stack),
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**ParamT, RetT](abc.ABC):

    @property
    @abc.abstractmethod
    def decoratee_t(self) -> type[Decoratee[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def connect_t(self) -> type[Connect[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def exit_t(self) -> type[Exit[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def enter_t(self) -> type[Enter[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def decorated_t(self) -> type[Decorated[typing.Any, typing.Any]]: ...

    def __call__(self, decoratee: Decoratee[ParamT, RetT], /) -> Decorated[ParamT, RetT]:
        return self.decorated_t(
            __doc__=str(decoratee.__doc__),
            __module__=str(decoratee.__module__),
            __name__=str(decoratee.__name__),
            __qualname__=str(decoratee.__qualname__),
            __signature__=inspect.signature(decoratee),
            decorator=self,
            stack=(self.enter_t(decorator=self, decoratee=decoratee),)
        )
