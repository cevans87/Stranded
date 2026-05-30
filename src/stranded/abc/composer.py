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
        return (Param(args=(value.ret,), kwargs={}) if isinstance(value, Return) else value,)

    async def call_async[SenderRetT](self, value: Composed.Value[ParamT, SenderRetT], /) -> Composed.Stack:
        return self.call_sync(value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT](abc.ABC):
    decorated: decorator.Decorated[ParamT, RetT]
    receiver: decorator.Decorated[typing.Any, typing.Any]

    @property
    @abc.abstractmethod
    def receive_t(self) -> type[Receive[typing.Any, typing.Any]]: ...

    def call_sync[**ReceiverParamT](self, value: Composed.Value[ReceiverParamT, RetT], /) -> Composed.Stack:
        return (Param(args=(value.ret,), kwargs={}) if isinstance(value, Return) else value,)

    async def call_async[**ReceiverParamT](self, value: Composed.Value[ReceiverParamT, RetT], /) -> Composed.Stack:
        return self.call_sync(value)


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
        | decorator.Decorated[typing.Any, typing.Any]
        | decorator.Decoratee[typing.Any, typing.Any],
        ...,
    ]
    type Value[**ParamT_, RetT_] = Param[ParamT_] | Raise | Return[RetT_] | Stop

    @property
    @abc.abstractmethod
    def receive_t(self) -> type[Receive[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def send_t(self) -> type[Send[typing.Any, typing.Any]]: ...

    # decorateds is stored in reverse execution order: decorateds[-1] runs first, decorateds[0] runs last.
    def __post_init__(self) -> None:
        ds = self.decorateds
        ordered = tuple(reversed(ds))
        object.__setattr__(self, '__doc__', '\n\n'.join(str(d.__doc__) for d in ordered))
        object.__setattr__(self, '__module__', ', '.join(str(d.__module__) for d in ordered))
        object.__setattr__(self, '__name__', ', '.join(str(d.__name__) for d in ordered))
        object.__setattr__(self, '__qualname__', ', '.join(str(d.__qualname__) for d in ordered))
        object.__setattr__(self, '__signature__', inspect.Signature().replace(
            parameters=list(ds[-1].__signature__.parameters.values()),
            return_annotation=ds[0].__signature__.return_annotation,
        ))

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
        return NotImplemented


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composer(abc.ABC):

    @property
    @abc.abstractmethod
    def receive_t(self) -> type[Receive[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def send_t(self) -> type[Send[typing.Any, typing.Any]]: ...
    @property
    @abc.abstractmethod
    def composed_t(self) -> type[Composed[typing.Any, typing.Any]]: ...

    def __call__(
        self,
        *decorateds: decorator.Decorated[typing.Any, typing.Any],
    ) -> Composed[typing.Any, typing.Any]:
        if not decorateds:
            raise exception_.Exception(f'{type(self).__name__} requires at least one decorated.')
        composed: Composed[typing.Any, typing.Any] = self.composed_t(composer=self, decorateds=(decorateds[0],))
        for decorated in decorateds[1:]:
            composed = composed | decorated
        return composed
