import abc
import dataclasses
import typing

from ..abc import composer_


Raise = composer_.Raise
Stop = composer_.Stop
Param = composer_.Param
Return = composer_.Return
type ValueT[**ParamT_, RetT_] = composer_.ValueT[ParamT_, RetT_]
type StackT = tuple[
    ValueT[typing.Any, typing.Any]
    | Composee[typing.Any, typing.Any]
    | Connect[typing.Any, typing.Any]
    | Exit[typing.Any, typing.Any]
    | Enter[typing.Any, typing.Any]
    | Composed[typing.Any, typing.Any],
    ...,
]


class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], typing.Protocol):
    def __call__(*args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], abc.ABC):
    def __call__(self, value: ValueT[ParamT, RetT], /) -> StackT: return super().__call__(value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer_.Exit[ParamT, RetT], abc.ABC):
    def __call__(self, value: ValueT[ParamT, RetT], /) -> StackT: return super().__call__(value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], abc.ABC):
    def __call__(self, value: ValueT[ParamT, RetT], /) -> StackT: return super().__call__(value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], abc.ABC):
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT:
        value: Param[ParamT] | Raise | Return[RetT] | Stop = Param(args=args, kwargs=kwargs)
        stack = list(self.stack)
        while stack:
            match stack.pop():
                case Param() | Raise() | Return() | Stop() as value_: value = value_
                case Enter() | Exit() | Connect() as get_stack_: stack += get_stack_(value)
                case Composed() as composed_ if isinstance(value, Param): stack += composed_.stack
                case composee_ if isinstance(value, Param):
                    try:
                        value = Return(ret=composee_(*value.args, **value.kwargs))
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
class Composer[**ParamT, RetT](composer_.Composer[ParamT, RetT]):
    composee_t: typing.ClassVar = Composee
    connect_t: typing.ClassVar = Connect
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    composed_t: typing.ClassVar = Composed
