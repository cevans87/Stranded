import abc
import dataclasses
import sys
import typing

from ..abc import decorator


@dataclasses.dataclass(frozen=True)
class Raise(decorator.Raise): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Param[**ParamT](decorator.Param[ParamT]): ...


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](decorator.Decoratee[ParamT, RetT], typing.Protocol):
    async def __call__(*args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Receive[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Send[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Exit[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    async def __call__(
        self,
        result: decorator.Raise | RetT,
    ) -> tuple[DecorateeT | typing.Self | EnterT | DecoratedT, ...]:
        return super().__call__(result)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Enter[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    async def __call__(
        self,
        *args: ParamT.args,
        **kwargs: ParamT.kwargs,
    ) -> tuple[DecorateeT | ExitT | typing.Self | DecoratedT, ...]:
        return super().__call__(*args, **kwargs)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorated[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
):
    async def __call__(self, *args: ParamT.args, **kwargs: ParamT.kwargs) -> RetT:
        result: decorator.Raise | RetT = ...
        stack = [self, *self.stack]
        while stack:
            match stack.pop():
                case Param(args=args, kwargs=kwargs): pass
                case Decorated() as decorated_: stack.extend(await decorated_.create_context())
                case Enter() as enter_: stack.extend(await enter_(*args, **kwargs))
                case Exit() as exit_: stack.extend(await exit_(result))
                case Send() as send_: stack.append(send_(result))
                case Receive() as receive_: stack.append(receive_(*args, **kwargs))
                case Decoratee() as decoratee_:
                    try:
                        result = await decoratee_(*args, **kwargs)
                    except Exception:  # noqa
                        result = decorator.Raise(*sys.exc_info())

        if isinstance(result, decorator.Raise):
            raise result.exc_val

        return result

    async def create_context(self) -> tuple[DecorateeT | ReceiveT | SendT | ExitT | EnterT | DecoratorT, ...]:
        return super().create_context()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorator[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
    abc.ABC,
): ...
