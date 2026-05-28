from __future__ import annotations

import abc
import dataclasses
import inspect
import typing

from . import decorator
from ..builtins import exception_


Param = decorator.Param
Raise = decorator.Raise
Return = decorator.Return
Stop = decorator.Stop


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](abc.ABC):
    decorated: decorator.Decorated[ParamT, RetT]
    sender: decorator.Decorated[typing.Any, typing.Any]

    def call_sync[SenderRetT](self, value: Composed.Value[ParamT, SenderRetT], /) -> Composed.Stack:
        return (
            self.decorated.enter_t(decorated=self.decorated),
            Param(args=(value.ret,), kwargs={}) if isinstance(value, Return) else value,
        )

    async def call_async[SenderRetT](self, value: Composed.Value[ParamT, SenderRetT], /) -> Composed.Stack:
        return self.call_sync(value)  # type: ignore[return-value]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT](abc.ABC):
    decorated: decorator.Decorated[ParamT, RetT]
    receiver: decorator.Decorated[typing.Any, typing.Any]

    def call_sync[**ReceiverParamT](self, value: Composed.Value[ReceiverParamT, RetT], /) -> Composed.Stack:
        return (
            self.receiver.enter_t(decorated=self.receiver),
            Param(args=(value.ret,), kwargs={}) if isinstance(value, Return) else value,
        )

    async def call_async[**ReceiverParamT](self, value: Composed.Value[ReceiverParamT, RetT], /) -> Composed.Stack:
        return self.call_sync(value)  # type: ignore[return-value]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](abc.ABC):
    composer: Composer
    decorateds: tuple[decorator.Decorated[typing.Any, RetT], ...]

    type Stack = tuple[
        Param[typing.Any]
        | Raise
        | Return[typing.Any]
        | Stop
        | decorator.Enter[typing.Any, typing.Any]
        | decorator.Exit[typing.Any, typing.Any]
        | Send[typing.Any, typing.Any]
        | Receive[typing.Any, typing.Any]
        | decorator.Decoratee[typing.Any, typing.Any],
        ...,
    ]
    type Value[**ParamT_, RetT_] = Param[ParamT_] | Raise | Return[RetT_] | Stop

    @property
    def __doc__(self) -> str:
        return '\n\n'.join(str(decorated.__doc__) for decorated in self.decorateds)

    @property
    def __module__(self) -> str:
        return ', '.join(str(decorated.__module__) for decorated in self.decorateds)

    @property
    def __name__(self) -> str:
        return ', '.join(str(decorated.__name__) for decorated in self.decorateds)

    @property
    def __qualname__(self) -> str:
        return ', '.join(str(decorated.__qualname__) for decorated in self.decorateds)

    @property
    def __signature__(self) -> inspect.Signature:
        return inspect.Signature().replace(
           parameters=list(self.decorateds[0].__signature__.parameters.values()),
           return_annotation=self.decorateds[-1].__signature__.return_annotation,
        )

    def __or__[**OtherParamT, OtherRetT](
        self,
        other: Composed[OtherParamT, OtherRetT] | decorator.Decorated[OtherParamT, OtherRetT],
        /,
    ) -> Composed[ParamT, OtherRetT]:
        match other:
            case Composed() as composed_:
                return dataclasses.replace(self, decorateds=(*composed_.decorateds, *self.decorateds))
            case decorator.Decorated() as decorated_:
                return dataclasses.replace(self, decorateds=(decorated_, *self.decorateds))


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composer(abc.ABC):

    @property
    @abc.abstractmethod
    def send_t(self) -> type[Send[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def receive_t(self) -> type[Receive[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def composed_t(self) -> type[Composed[typing.Any, typing.Any]]: ...

    def __call__[**ParamT, RetT](self, decorated: decorator.Decorated[ParamT, RetT], /) -> Composed[ParamT, RetT]:
        return self.composed_t(
            __doc__=decorated.__doc__,
            __module__=decorated.__module__,
            __name__=decorated.__name__,
            __qualname__=decorated.__qualname__,
            __signature__=decorated.__signature__,
            composer=self,
            decorateds=(decorated,),
        )
