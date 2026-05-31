import dataclasses
import typing

from .abc import argument_parser_
from .. import composer


@dataclasses.dataclass(frozen=True, kw_only=True)
class ArgumentParser(  # type: ignore[misc]
    composer.Composer[..., typing.Any],
    argument_parser_.ArgumentParser[..., typing.Any],
): ...


Composer = ArgumentParser
argument_parser = ArgumentParser()
