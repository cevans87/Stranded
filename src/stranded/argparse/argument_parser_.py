import dataclasses
import typing

from .abc import argument_parser_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class ArgumentParser(  # type: ignore[misc]
    decorator.Decorator[..., typing.Any],
    argument_parser_.ArgumentParser[..., typing.Any],
): ...


Decorator = ArgumentParser
argument_parser = ArgumentParser()
