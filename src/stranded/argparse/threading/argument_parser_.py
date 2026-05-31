from __future__ import annotations

import asyncio
import dataclasses
import inspect
import typing

from ...threading import composer
from ..abc import argument_parser_

@typing.runtime_checkable
class Composee[**ParamT, RetT](composer.Composee[ParamT, RetT], argument_parser_.Composee[ParamT, RetT], typing.Protocol): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer.Connect[ParamT, RetT], argument_parser_.Connect[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer.Exit[ParamT, RetT], argument_parser_.Exit[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer.Enter[ParamT, RetT], argument_parser_.Enter[ParamT, RetT]): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer.Composed[ParamT, RetT], argument_parser_.Composed[ParamT, RetT]):
    def __call__(self, *argv: str) -> RetT:  # type: ignore[override]
        ret = None
        for call in super(composer.Composed, self).__call__(*argv):
            ret = call()
            if inspect.iscoroutine(ret):
                ret = asyncio.run(ret)
        return ret  # type: ignore[return-value]


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class ArgumentParser[**ParamT, RetT](composer.Composer[ParamT, RetT], argument_parser_.Composer[ParamT, RetT]):
    composee_t: typing.ClassVar = Composee
    connect_t: typing.ClassVar = Connect
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    composed_t: typing.ClassVar = Composed
Composer = ArgumentParser
argument_parser: ArgumentParser[..., typing.Any] = ArgumentParser()
