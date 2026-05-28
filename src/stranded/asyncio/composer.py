import abc
import dataclasses
import inspect
import sys
import typing

from ..abc import composer, decorator
from ..builtins import exception_


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
    """Async-only Composed — assumes the caller is in an async context.

    Awaits any awaitable Enter/Exit/Decoratee result. Sync Decorateds simply
    run inline (no `asyncio.run`, no thread offload).
    """

    async def call_async(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT:
        value: Param[ParamT] | Raise | Return[RetT] | Stop = Param(args=args, kwargs=kwargs)
        stack = [*self.decorateds]
        while stack:
            match popped := stack.pop():
                case Param() | Raise() | Return() | Stop(): value = popped
                case decorator.Enter() | decorator.Exit():
                    extension: typing.Any = popped(value)
                    if inspect.isawaitable(extension):
                        extension = await extension
                    stack += extension
                case Send() | Receive(): value = await popped.call_async(value)  # type: ignore[assignment]
                case decorator.Decorated() if isinstance(value, Param) and stack:
                    stack += [
                        self.composer.send_t(decorated=popped, receiver=stack[-1]),
                        popped.enter_t(decorated=popped),
                    ]
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
