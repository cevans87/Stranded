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
    | Composee[typing.Any, typing.Any]
    | Connect[typing.Any, typing.Any]
    | Exit[typing.Any, typing.Any]
    | Enter[typing.Any, typing.Any]
    | Composed[typing.Any, typing.Any],
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


class Composee[**ParamT, RetT](typing.Protocol):
    __doc__: str
    __module__: str
    __name__: str
    __qualname__: str
    __signature__: inspect.Signature
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT: ...
    def __get__(self, instance: Instance, owner: type[object] | None) -> typing.Self: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](abc.ABC):
    composer: Composer[ParamT, RetT]
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
    def composer(self) -> Composer[typing.Any, typing.Any]: return self.enter.composer
    @property
    def composee_t(self) -> type[Composee[typing.Any, typing.Any]]: return self.composer.composee_t
    @property
    def exit_t(self) -> type[Exit[typing.Any, typing.Any]]: return self.composer.exit_t
    @property
    def enter_t(self) -> type[Enter[typing.Any, typing.Any]]: return self.composer.enter_t
    @property
    def composed_t(self) -> type[Composed[typing.Any, typing.Any]]: return self.composer.composed_t

    def __call__(self, value: ValueT[ParamT, RetT], /) -> StackT:
        return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](abc.ABC):
    composer: Composer[ParamT, RetT]
    composee: Composee[ParamT, RetT]

    @property
    def composee_t(self) -> type[Composee[typing.Any, typing.Any]]: return self.composer.composee_t
    @property
    def exit_t(self) -> type[Exit[typing.Any, typing.Any]]: return self.composer.exit_t
    @property
    def enter_t(self) -> type[Enter[typing.Any, typing.Any]]: return self.composer.enter_t
    @property
    def composed_t(self) -> type[Composed[typing.Any, typing.Any]]: return self.composer.composed_t

    def __call__(self, value: ValueT[ParamT, RetT], /) -> StackT:
        match value, self.composee:
            case Param(), Composed() as composed_: return self.exit_t(enter=self), *composed_.stack
            case Param(), composee_: return self.exit_t(enter=self), composee_,
            case _: return ()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](abc.ABC):
    __doc__: str
    __module__: str
    __name__: str
    __qualname__: str
    __signature__: inspect.Signature
    stack: StackT
    composer: Composer[ParamT, RetT]

    @property
    def composee_t(self) -> type[Composee[typing.Any, typing.Any]]: return self.composer.composee_t
    @property
    def connect_t(self) -> type[Connect[typing.Any, typing.Any]]: return self.composer.connect_t
    @property
    def exit_t(self) -> type[Exit[typing.Any, typing.Any]]: return self.composer.exit_t
    @property
    def enter_t(self) -> type[Enter[typing.Any, typing.Any]]: return self.composer.enter_t
    @property
    def composed_t(self) -> type[Composed[typing.Any, typing.Any]]: return self.composer.composed_t

    @property
    def composee(self) -> Composee[ParamT, RetT]:
        # The composee lives on the Enter at the base of the stack. Sub-domain code that
        # used to read self.composed.composee now reads it through this accessor.
        match self.stack:
            case [*_, Enter() as enter_]: return enter_.composee
        assert False, "unreachable"

    def __get__(self, instance: Instance, owner: type[object] | None) -> typing.Self:
        match self.stack:
            case [*_, Enter() as enter_]:
                return dataclasses.replace(
                    self,
                    stack=(
                        *self.stack[:-1],
                        dataclasses.replace(enter_, composee=enter_.composee.__get__(instance, owner)),
                    )
                )
        assert False, "unreachable"

    def __or__[**OtherParamT, OtherRetT](
        self,
        other_composed: Composed[OtherParamT, OtherRetT],
        /,
    ) -> Composed[ParamT, OtherRetT]:
        return dataclasses.replace(
            other_composed,
            __doc__=f"{self.__doc__}\n\n{other_composed.__doc__}",
            __name__=f"{self.__name__}|{other_composed.__name__}",
            __qualname__=f"{self.__qualname__}|{other_composed.__qualname__}",
            __signature__=inspect.Signature().replace(
                parameters=self.__signature__.parameters,
                return_annotation=other_composed.__signature__.return_annotation,
            ),
            stack=(self.connect_t(composer=self.composer, stack=other_composed.stack), *self.stack),
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composer[**ParamT, RetT](abc.ABC):

    @property
    @abc.abstractmethod
    def composee_t(self) -> type[Composee[typing.Any, typing.Any]]: ...
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
    def composed_t(self) -> type[Composed[typing.Any, typing.Any]]: ...

    def __call__(self, composee: Composee[ParamT, RetT], /) -> Composed[ParamT, RetT]:
        return self.composed_t(
            __doc__=str(composee.__doc__),
            __module__=str(composee.__module__),
            __name__=str(composee.__name__),
            __qualname__=str(composee.__qualname__),
            __signature__=inspect.signature(composee),
            composer=self,
            stack=(self.enter_t(composer=self, composee=composee),)
        )
