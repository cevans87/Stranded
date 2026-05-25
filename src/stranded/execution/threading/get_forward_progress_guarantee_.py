import dataclasses
import typing

from ..abc import get_forward_progress_guarantee_
from ...threading import decorator


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    get_forward_progress_guarantee_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT](
    decorator.Send[ParamT, RetT],
    get_forward_progress_guarantee_.Send[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](
    decorator.Receive[ParamT, RetT],
    get_forward_progress_guarantee_.Receive[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    get_forward_progress_guarantee_.Exit[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    get_forward_progress_guarantee_.Enter[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    get_forward_progress_guarantee_.Decorated[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class GetForwardProgressGuarantee[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    get_forward_progress_guarantee_.Decorator[ParamT, RetT],
): ...


Decorator = GetForwardProgressGuarantee
get_forward_progress_guarantee: GetForwardProgressGuarantee[..., typing.Any] = GetForwardProgressGuarantee()