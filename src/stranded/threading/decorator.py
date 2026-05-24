import abc
import dataclasses
import sys
import typing

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
class Receive[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Receive[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    def __call__[SRetT, **SParamT](  # type: ignore[override]
        self,
        value: Param[ParamT] | Raise | Return[SRetT] | Stop,
        /,
    ) -> Param[ParamT] | Raise | Param[typing.Concatenate[SRetT, SParamT]] | Stop:
        return super().__call__(value)  # type: ignore[return-value]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Send[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    def __call__[**RParamT](  # type: ignore[override]
        self,
        value: Param[ParamT] | Raise | Return[RetT] | Stop,
        /,
    ) -> Param[ParamT] | Raise | Param[typing.Concatenate[RetT, RParamT]] | Stop:
        return super().__call__(value)  # type: ignore[return-value]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Exit[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    @typing.overload  # type: ignore[override]
    def __call__(self, value: Param[ParamT], /) -> tuple[ExitT, DecorateeT]: ...
    @typing.overload
    def __call__(self, value: Raise | Return[RetT] | Stop, /) -> tuple[()]: ...
    def __call__(self, value: Param[ParamT] | Raise | Return[RetT] | Stop, /) -> tuple[ExitT, DecorateeT] | tuple[()]:
        return super().__call__(value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Enter[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    @typing.overload
    def __call__(self, value: Param[ParamT], /) -> tuple[ExitT, DecorateeT]: ...
    @typing.overload
    def __call__(self, value: Raise | Return[RetT] | Stop, /) -> tuple[()]: ...
    def __call__(self, value: Param[ParamT] | Raise | Return[RetT] | Stop, /) -> tuple[ExitT, DecorateeT] | tuple[()]:
        return super().__call__(value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorated[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT:
        value: Param[ParamT] | Raise | Return[RetT] | Stop | DecorateeT = Param(args=args, kwargs=kwargs)
        stack = [*self.create_context(), *self.stack]
        while stack:
            match popped := stack.pop():
                case Param() | Raise() | Return() | Stop(): value = popped
                case Enter() | Exit(): stack.extend(popped(value))  # type: ignore[arg-type]
                case Send() | Receive(): value = popped(value)  # type: ignore[arg-type]
                case Decoratee() if isinstance(value, Param):
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

    def create_context(self) -> tuple[DecorateeT | ReceiveT | SendT | ExitT | EnterT | DecoratorT, ...]:
        return super().create_context()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorator[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...
