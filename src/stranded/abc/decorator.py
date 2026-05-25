from __future__ import annotations

import abc
import dataclasses
import inspect
import types
import typing

if typing.TYPE_CHECKING:
    from . import composer as _composer

type Instance = object


@dataclasses.dataclass(frozen=True)
class Raise:
    exc_type: type[BaseException]
    exc_val: BaseException
    exc_tb: types.TracebackType


@dataclasses.dataclass(frozen=True)
class Stop(BaseException): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Param[**ParamT]:
    args: ParamT.args
    kwargs: ParamT.kwargs


@dataclasses.dataclass(frozen=True)
class Return[RetT]:
    ret: RetT


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](typing.Protocol):
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT: ...
    def __get__(self, instance: Instance, owner: type[object] | None) -> typing.Self: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](abc.ABC):
    # Sub-domain code subclasses this for parallel structure with Send/Exit/Enter.
    # The composition pipeline does NOT use these instances; it uses composer.Receive
    # (which holds a Composed reference rather than a Decorated reference).
    decorated: Decorated[ParamT, RetT]

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
class Send[**ParamT, RetT](abc.ABC):
    decorated: Decorated[ParamT, RetT]

    def __call__[**RParamT](
        self,
        value: Param[ParamT] | Raise | Return[RetT] | Stop,
        /,
    ) -> Param[ParamT] | Raise | Param[typing.Concatenate[RetT, RParamT]] | Stop:
        match value:
            case Param() as param_: return param_
            case Raise() as raise_: return raise_
            case Return() as return_: return Param(args=(return_.ret,), kwargs={})
            case Stop() as stop_: return stop_


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

    def __call__(self, value: Param[ParamT] | Raise | Return[RetT] | Stop) -> tuple[()]:
        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](abc.ABC):
    decorated: Decorated[ParamT, RetT]

    @property
    def decorator(self) -> Decorator[typing.Any, typing.Any]: return self.decorated.decorator
    @property
    def decoratee_t(self) -> type[Decoratee[typing.Any, typing.Any]]: return self.decorator.decoratee_t
    @property
    def exit_t(self) -> type[Exit[typing.Any, typing.Any]]: return self.decorator.exit_t
    @property
    def enter_t(self) -> type[Enter[typing.Any, typing.Any]]: return self.decorator.enter_t
    @property
    def decorated_t(self) -> type[Decorated[typing.Any, typing.Any]]: return self.decorator.decorated_t

    @typing.overload
    def __call__(self, value: Param[ParamT], /) -> tuple[Exit[ParamT, RetT], Decoratee[ParamT, RetT]]: ...
    @typing.overload
    def __call__(self, value: Raise | Return[RetT] | Stop, /) -> tuple[()]: ...
    def __call__(
        self, value: Param[ParamT] | Raise | Return[RetT] | Stop, /,
    ) -> tuple[Exit[ParamT, RetT], Decoratee[ParamT, RetT]] | tuple[()]:
        match value:
            case Param(): return self.exit_t(enter=self), self.decorated.decoratee,
            case _: return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](abc.ABC):
    __doc__: str
    __module__: str
    __name__: str
    __qualname__: str
    __signature__: inspect.Signature
    decoratee: Decoratee[ParamT, RetT]
    decorator: Decorator[ParamT, RetT]

    @property
    def decoratee_t(self) -> type[Decoratee[typing.Any, typing.Any]]: return self.decorator.decoratee_t
    @property
    def exit_t(self) -> type[Exit[typing.Any, typing.Any]]: return self.decorator.exit_t
    @property
    def enter_t(self) -> type[Enter[typing.Any, typing.Any]]: return self.decorator.enter_t
    @property
    def decorated_t(self) -> type[Decorated[typing.Any, typing.Any]]: return self.decorator.decorated_t

    def __get__(self, instance: Instance, owner: type[object] | None) -> typing.Self:
        return dataclasses.replace(self, decoratee=self.decoratee.__get__(instance, owner))


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**ParamT, RetT](abc.ABC):

    @property
    @abc.abstractmethod
    def decoratee_t(self) -> type[Decoratee[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def exit_t(self) -> type[Exit[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def enter_t(self) -> type[Enter[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def decorated_t(self) -> type[Decorated[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def composer_t(self) -> type[_composer.Composer]: ...

    def __call__(self, decoratee: Decoratee[ParamT, RetT], /) -> Decorated[ParamT, RetT]:
        return self.decorated_t(
            __doc__=str(decoratee.__doc__),
            __module__=str(decoratee.__module__),
            __name__=str(decoratee.__name__),  # type: ignore[attr-defined]
            __qualname__=str(decoratee.__qualname__),  # type: ignore[attr-defined]
            __signature__=inspect.signature(decoratee),
            decoratee=decoratee,
            decorator=self,
        )
