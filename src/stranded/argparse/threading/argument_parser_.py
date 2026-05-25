from __future__ import annotations

import asyncio
import dataclasses
import inspect
import typing

from ...threading import decorator
from ..abc import argument_parser_

@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    argument_parser_.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Send[**ParamT, RetT](
    decorator.Send[ParamT, RetT],
    argument_parser_.Send[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Receive[**ParamT, RetT](
    decorator.Receive[ParamT, RetT],
    argument_parser_.Receive[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](
    decorator.Exit[ParamT, RetT],
    argument_parser_.Exit[ParamT, RetT],
): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](
    decorator.Enter[ParamT, RetT],
    argument_parser_.Enter[ParamT, RetT],
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    argument_parser_.Decorated[ParamT, RetT],
):
    def __call__(self, *argv: str) -> RetT:  # type: ignore[override]
        ret = None
        for call in super(decorator.Decorated, self).__call__(*argv):
            ret = call()
            if inspect.iscoroutine(ret):
                ret = asyncio.run(ret)
        return ret  # type: ignore[return-value]


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class ArgumentParser[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    argument_parser_.Decorator[ParamT, RetT],
):
    decoratee_t: typing.ClassVar = Decoratee
    receive_t: typing.ClassVar = Receive
    send_t: typing.ClassVar = Send
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    decorated_t: typing.ClassVar = Decorated
Decorator = ArgumentParser
argument_parser: ArgumentParser[..., typing.Any] = ArgumentParser()
