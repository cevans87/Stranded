import abc
import dataclasses
import sys
import typing

from . import composer
from ..abc import decorator
from ..builtins import exception_


Raise = decorator.Raise
Stop = decorator.Stop
Param = decorator.Param
Return = decorator.Return


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](decorator.Decoratee[ParamT, RetT], typing.Protocol):
    def __call__(*args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](decorator.Receive[ParamT, RetT], abc.ABC):
    def __call__[SRetT, **SParamT](  # type: ignore[override]
        self,
        value: Param[ParamT] | Raise | Return[SRetT] | Stop,
        /,
    ) -> Param[ParamT] | Raise | Param[typing.Concatenate[SRetT, SParamT]] | Stop:
        return super().__call__(value)  # type: ignore[return-value]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT](decorator.Send[ParamT, RetT], abc.ABC):
    def __call__[**RParamT](  # type: ignore[override]
        self,
        value: Param[ParamT] | Raise | Return[RetT] | Stop,
        /,
    ) -> Param[ParamT] | Raise | Param[typing.Concatenate[RetT, RParamT]] | Stop:
        return super().__call__(value)  # type: ignore[return-value]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](decorator.Exit[ParamT, RetT], abc.ABC):
    @typing.overload  # type: ignore[override]
    def __call__(self, value: Param[ParamT], /) -> tuple[decorator.Exit[ParamT, RetT], decorator.Decoratee[ParamT, RetT]]: ...
    @typing.overload
    def __call__(self, value: Raise | Return[RetT] | Stop, /) -> tuple[()]: ...
    def __call__(
        self, value: Param[ParamT] | Raise | Return[RetT] | Stop, /,
    ) -> tuple[decorator.Exit[ParamT, RetT], decorator.Decoratee[ParamT, RetT]] | tuple[()]:
        return super().__call__(value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](decorator.Enter[ParamT, RetT], abc.ABC):
    @typing.overload
    def __call__(self, value: Param[ParamT], /) -> tuple[decorator.Exit[ParamT, RetT], decorator.Decoratee[ParamT, RetT]]: ...
    @typing.overload
    def __call__(self, value: Raise | Return[RetT] | Stop, /) -> tuple[()]: ...
    def __call__(
        self, value: Param[ParamT] | Raise | Return[RetT] | Stop, /,
    ) -> tuple[decorator.Exit[ParamT, RetT], decorator.Decoratee[ParamT, RetT]] | tuple[()]:
        return super().__call__(value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](decorator.Decorated[ParamT, RetT], abc.ABC):
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT:
        value: Param[ParamT] | Raise | Return[RetT] | Stop = Param(args=args, kwargs=kwargs)
        stack: list[typing.Any] = [self]
        while stack:
            match popped := stack.pop():
                case Param() | Raise() | Return() | Stop(): value = popped
                case Enter() | Exit(): stack += popped(value)
                case decorator.Decorated() if isinstance(value, Param): stack.append(popped.enter_t(decorated=popped))
                case decorator.Decoratee() if isinstance(value, Param):
                    try:
                        value = Return(ret=popped(*value.args, **value.kwargs))
                    except Stop as stopped:
                        value = stopped
                    except Exception:
                        value = Raise(*sys.exc_info())

        match value:
            case Stop() as stop_: raise stop_
            case Raise() as raise_: raise raise_.exc_val
            case Return() as return_: return return_.ret  # type: ignore[no-any-return]
            case _: raise exception_.Exception(f'{type(self).__name__} call completed with invalid {value=!r}')


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**ParamT, RetT](decorator.Decorator[ParamT, RetT]):
    decoratee_t: typing.ClassVar = Decoratee
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    decorated_t: typing.ClassVar = Decorated
    composer_t: typing.ClassVar = composer.Composer
