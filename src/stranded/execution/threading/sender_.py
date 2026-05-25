import abc
import dataclasses
import typing

from ..abc import sender_
from . import operation_state_
from . import receiver_
from ...threading import decorator


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    sender_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT](
    decorator.Send[ParamT, RetT],
    sender_.Send[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](
    decorator.Receive[ParamT, RetT],
    sender_.Receive[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    sender_.Exit[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    sender_.Enter[ParamT, RetT],
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    sender_.Decorated[ParamT, RetT],
    abc.ABC,
):
    @abc.abstractmethod
    def connect(
        self,
        receiver: receiver_.Decorated[..., typing.Any],
        /,
    ) -> operation_state_.Decorated[..., typing.Any]: ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    sender_.Decorator[ParamT, RetT],
): ...


sender: Decorator[..., typing.Any] = Decorator()