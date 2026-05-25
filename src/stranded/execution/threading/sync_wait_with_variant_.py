import dataclasses
import typing

from ..abc import sync_wait_with_variant_
from ...threading import decorator


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    sync_wait_with_variant_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT](
    decorator.Send[ParamT, RetT],
    sync_wait_with_variant_.Send[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](
    decorator.Receive[ParamT, RetT],
    sync_wait_with_variant_.Receive[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    sync_wait_with_variant_.Exit[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    sync_wait_with_variant_.Enter[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    sync_wait_with_variant_.Decorated[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class SyncWaitWithVariant[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    sync_wait_with_variant_.Decorator[ParamT, RetT],
):
    decoratee_t: typing.ClassVar = Decoratee
    receive_t: typing.ClassVar = Receive
    send_t: typing.ClassVar = Send
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    decorated_t: typing.ClassVar = Decorated
Decorator = SyncWaitWithVariant
sync_wait_with_variant: SyncWaitWithVariant[..., typing.Any] = SyncWaitWithVariant()