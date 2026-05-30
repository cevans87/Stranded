import abc
import dataclasses
import typing

from . import composer
from ..abc import decorator


Raise = decorator.Raise
Stop = decorator.Stop
Param = decorator.Param
Return = decorator.Return
ValueT = decorator.ValueT
type StackT = tuple[
    ValueT[typing.Any, typing.Any]
    | Decoratee[typing.Any, typing.Any]
    | Connect[typing.Any, typing.Any]
    | Exit[typing.Any, typing.Any]
    | Enter[typing.Any, typing.Any]
    | Decorated[typing.Any, typing.Any],
    ...,
]


class Decoratee[**ParamT, RetT](decorator.Decoratee[ParamT, RetT], typing.Protocol):
    def __call__(*args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](decorator.Connect[ParamT, RetT], abc.ABC):
    def __call__( self, value: ValueT, /) -> StackT: return super().__call__(value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](decorator.Exit[ParamT, RetT], abc.ABC):
    def __call__( self, value: ValueT, /) -> StackT: return super().__call__(value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](decorator.Enter[ParamT, RetT], abc.ABC):
    def __call__(self, value: ValueT, /) -> StackT: return super().__call__(value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](decorator.Decorated[ParamT, RetT], abc.ABC):
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT:
        value: Param[ParamT] | Raise | Return[RetT] | Stop = Param(args=args, kwargs=kwargs)
        stack = list(self.stack)
        while stack:
            match stack.pop():
                case Param() | Raise() | Return() | Stop() as value_: value = value_
                case Enter() | Exit() | Connect() as get_stack_: stack += get_stack_(value)
                case Decorated() as decorated_ if isinstance(value, Param): stack += decorated_.stack
                case decoratee_ if isinstance(value, Param):
                    try:
                        value = Return(ret=decoratee_(*value.args, **value.kwargs))
                    except Stop as stopped_:
                        value = stopped_
                    except Exception as exception_:
                        value = Raise(exc_type=type(exception_), exc_val=exception_, exc_tb=exception_.__traceback__)

        match value:
            case Stop() as stop_: raise stop_
            case Raise() as raise_: raise raise_.exc_val
            case Return() as return_: return return_.ret  # type: ignore[no-any-return]
            case _: raise Exception(f'{type(self).__name__} call completed with invalid {value=!r}')


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**ParamT, RetT](decorator.Decorator[ParamT, RetT]):
    decoratee_t: typing.ClassVar = Decoratee
    connect_t: typing.ClassVar = Connect
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    decorated_t: typing.ClassVar = Decorated
    composer_t: typing.ClassVar = composer.Composer
