import dataclasses

from .abc_ import cli
from . import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Cli(decorator.Decorator, cli.Decorator): ...
