import dataclasses
import typing

from . import decorator
from .abc import get_domain_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetDomain(
    decorator.Decorator[..., typing.Any],
    get_domain_.GetDomain[..., typing.Any],
): ...


Decorator = GetDomain
get_domain = GetDomain()
