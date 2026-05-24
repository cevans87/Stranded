import dataclasses
import typing

from .abc import argument_parser_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class ArgumentParser(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    argument_parser_.ArgumentParser[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = ArgumentParser
argument_parser = ArgumentParser()
