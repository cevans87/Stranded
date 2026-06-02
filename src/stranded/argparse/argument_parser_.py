import dataclasses
import typing

from .abc import argument_parser_
from .. import composer_


@dataclasses.dataclass(frozen=True, kw_only=True)
class ArgumentParser(composer_.Composer[..., typing.Any], argument_parser_.ArgumentParser[..., typing.Any]): ...  # type: ignore[misc]


Composer = ArgumentParser
argument_parser = ArgumentParser()
