import dataclasses
import typing


@dataclasses.dataclass(frozen=True, kw_only=True)
class Constraint[T]:
    _assert: typing.Callable[[T], bool]
