import dataclasses
import inspect
import typing

from ...asyncio import composer_
from ..abc import argument_parser_

@typing.runtime_checkable
class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], argument_parser_.Composee[ParamT, RetT], typing.Protocol): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], argument_parser_.Connect[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer_.Exit[ParamT, RetT], argument_parser_.Exit[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], argument_parser_.Enter[ParamT, RetT]): ...


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], argument_parser_.Composed[ParamT, RetT]):
    async def __call__(self, *argv: str) -> RetT:  # type: ignore[override]
        ret = None
        for call in super(composer_.Composed, self).__call__(*argv):
            ret = call()
            if inspect.iscoroutine(ret):
                ret = await ret
        return ret  # type: ignore[return-value]


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class ArgumentParser[**ParamT = ..., RetT = typing.Any](composer_.Composer[ParamT, RetT], argument_parser_.Composer[ParamT, RetT]):
    composee_t: typing.ClassVar = Composee
    connect_t: typing.ClassVar = Connect
    exit_t: typing.ClassVar = Exit
    enter_t: typing.ClassVar = Enter
    composed_t: typing.ClassVar = Composed


Composer = ArgumentParser
argument_parser = ArgumentParser()
