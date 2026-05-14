import dataclasses

from .abc import argument_parser
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class ArgumentParser(decorator.Decorator, argument_parser.Decorator): ...
