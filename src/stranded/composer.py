import abc
import asyncio
import dataclasses
import inspect
import sys
import typing

from .abc import composer, decorator
from .builtins import exception_


Param = composer.Param
Raise = composer.Raise
Return = composer.Return
Stop = composer.Stop


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT](composer.Send[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](composer.Receive[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer.Composed[ParamT, RetT], abc.ABC):
    """Agnostic Composed — supports both sync and async entry.

    `call_sync` ``asyncio.run``s any awaitable returned by an Enter/Exit or
    Decoratee, so async Decorateds work from a sync caller.

    `call_async` ``await``s any awaitable, and runs sync Decorateds inline.
    """

    def call_sync(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT:
        value: Param[ParamT] | Raise | Return[RetT] | Stop = Param(args=args, kwargs=kwargs)
        stack: list[typing.Any] = list(self.stack)
        while stack:
            match popped := stack.pop():
                case Param() | Raise() | Return() | Stop(): value = popped
                case decorator.Enter() | decorator.Exit():
                    extension: typing.Any = popped(value)
                    if inspect.isawaitable(extension):
                        extension = asyncio.run(extension)  # type: ignore[arg-type]
                    stack.extend(extension)
                case Send() | Receive(): value = popped.call_sync(value)  # type: ignore[assignment]
                case decorator.Decoratee() if isinstance(value, Param):
                    try:
                        ret: typing.Any = popped(*value.args, **value.kwargs)
                        if inspect.isawaitable(ret):
                            ret = asyncio.run(ret)  # type: ignore[arg-type]
                        value = Return(ret=ret)
                    except Stop as stopped:
                        value = stopped
                    except Exception:
                        value = Raise(*sys.exc_info())

        match value:
            case Stop() as stop_: raise stop_
            case Raise() as raise_: raise raise_.exc_val
            case Return() as return_: return return_.ret  # type: ignore[no-any-return]
            case _: raise exception_.Exception(f'{type(self).__name__} call completed with invalid {value=!r}')

    async def call_async(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT:
        value: Param[ParamT] | Raise | Return[RetT] | Stop = Param(args=args, kwargs=kwargs)
        stack: list[typing.Any] = list(self.stack)
        while stack:
            match popped := stack.pop():
                case Param() | Raise() | Return() | Stop(): value = popped
                case decorator.Enter() | decorator.Exit():
                    extension: typing.Any = popped(value)
                    if inspect.isawaitable(extension):
                        extension = await extension
                    stack.extend(extension)
                case Send() | Receive(): value = await popped.call_async(value)  # type: ignore[assignment]
                case decorator.Decoratee() if isinstance(value, Param):
                    try:
                        ret: typing.Any = popped(*value.args, **value.kwargs)
                        if inspect.isawaitable(ret):
                            ret = await ret
                        value = Return(ret=ret)
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
class Composer(composer.Composer):
    send_t: typing.ClassVar = Send
    receive_t: typing.ClassVar = Receive
    composed_t: typing.ClassVar = Composed
