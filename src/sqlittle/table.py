import dataclasses

from .abc_ import table as abc_table
from funktools import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Table(decorator.Decorator, abc_table.Decorator): ...
