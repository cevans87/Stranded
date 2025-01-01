import dataclasses

from .abc_ import argument_parser
from funktools import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class ArgumentParser(decorator.Decorator, argument_parser.Decorator): ...
