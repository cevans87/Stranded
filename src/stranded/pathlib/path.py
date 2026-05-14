import dataclasses

from .abc import path as abc_path
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Path(decorator.Decorator, abc_path.Decorator): ...
