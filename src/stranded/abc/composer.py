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
    composed: Composed[typing.Any, typing.Any]

    def call_sync[SRetT, **SParamT](
        self,
        value: Param[ParamT] | Raise | Return[SRetT] | Stop,
        /,
    ) -> Param[ParamT] | Raise | Param[typing.Concatenate[SRetT, SParamT]] | Stop:
        match value:
            case Param() as param_: return param_
            case Raise() as raise_: return raise_
            case Return() as return_: return Param(args=(return_.ret,), kwargs={})  # noqa
            case Stop() as stop_: return stop_

    async def call_async[SRetT, **SParamT](
        self,
        value: Param[ParamT] | Raise | Return[SRetT] | Stop,
        /,
    ) -> Param[ParamT] | Raise | Param[typing.Concatenate[SRetT, SParamT]] | Stop:
        return self.call_sync(value)  # type: ignore[return-value]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT](abc.ABC):
    composed: Composed[typing.Any, typing.Any]

    def call_sync[**RParamT](
        self,
        value: Param[ParamT] | Raise | Return[RetT] | Stop,
        /,
    ) -> Param[ParamT] | Raise | Param[typing.Concatenate[RetT, RParamT]] | Stop:
        match value:
            case Param() as param_: return param_
            case Raise() as raise_: return raise_
            case Return() as return_: return Param(args=(return_.ret,), kwargs={})
            case Stop() as stop_: return stop_

    async def call_async[**RParamT](
        self,
        value: Param[ParamT] | Raise | Return[RetT] | Stop,
        /,
    ) -> Param[ParamT] | Raise | Param[typing.Concatenate[RetT, RParamT]] | Stop:
        return self.call_sync(value)  # type: ignore[return-value]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](abc.ABC):
    __doc__: str
    __module__: str
    __name__: str
    __qualname__: str
    __signature__: inspect.Signature
    composer: Composer
    decorateds: tuple[decorator.Decorated[typing.Any, typing.Any], ...]

    @property
    def stack(self) -> tuple[
        decorator.Enter[typing.Any, typing.Any]
        | decorator.Exit[typing.Any, typing.Any]
        | Send[typing.Any, typing.Any]
        | Receive[typing.Any, typing.Any], ...
    ]:
        # Build execution-order events for decorateds = [d0, d1, ..., dN]:
        #   d0.enter, d0.send, d1.receive, d1.enter, d1.send, d2.receive, ..., dN.enter
        # Stack is the reverse so list.pop() yields execution order.
        pops: list[
            decorator.Enter[typing.Any, typing.Any]
            | Send[typing.Any, typing.Any]
            | Receive[typing.Any, typing.Any]
        ] = []
        for i, decorated in enumerate(self.decorateds):
            if i > 0:
                pops.append(self.composer.send_t(composed=self))
                pops.append(self.composer.receive_t(composed=self))
            pops.append(decorated.decorator.enter_t(decorated=decorated))
        return tuple(reversed(pops))

    def __or__[**Param2T, Ret2T](
        self,
        other: Composed[Param2T, Ret2T] | decorator.Decorated[Param2T, Ret2T],
        /,
    ) -> Composed[ParamT, Ret2T]:
        match other:
            case Composed(): more = other.decorateds
            case decorator.Decorated(): more = (other,)
            case _: return NotImplemented
        return self.composer(*self.decorateds, *more)


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

    def __call__[**Param1T, Ret1T, **Param2T, Ret2T](
        self,
        *decorateds: decorator.Decorated[typing.Any, typing.Any],
    ) -> Composed[Param1T, Ret2T]:
        if not decorateds:
            raise exception_.Exception(f'{type(self).__name__} requires at least one decorated.')
        first, last = decorateds[0], decorateds[-1]
        return self.composed_t(
            __doc__='\n\n'.join(str(d.__doc__) for d in decorateds),
            __module__=', '.join(str(d.__module__) for d in decorateds),
            __name__=', '.join(str(d.__name__) for d in decorateds),
            __qualname__=', '.join(str(d.__qualname__) for d in decorateds),
            __signature__=inspect.Signature().replace(
                parameters=list(first.__signature__.parameters.values()),
                return_annotation=last.__signature__.return_annotation,
            ),
            composer=self,
            decorateds=tuple(decorateds),
        )
