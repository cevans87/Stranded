import dataclasses
import typing

from ..abc import inplace_stop_token_
from ...asyncio import decorator


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    inplace_stop_token_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT](
    decorator.Send[ParamT, RetT],
    inplace_stop_token_.Send[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](
    decorator.Receive[ParamT, RetT],
    inplace_stop_token_.Receive[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    inplace_stop_token_.Exit[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    inplace_stop_token_.Enter[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    inplace_stop_token_.Decorated[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class InplaceStopToken[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    inplace_stop_token_.Decorator[ParamT, RetT],
): ...


Decorator = InplaceStopToken
inplace_stop_token: InplaceStopToken[..., typing.Any] = InplaceStopToken()