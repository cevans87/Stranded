import dataclasses
import typing

from . import decorator
from .abc import default_domain_


@dataclasses.dataclass(frozen=True, kw_only=True)
class DefaultDomain(
    decorator.Decorator[..., typing.Any],
    default_domain_.DefaultDomain[..., typing.Any],
): ...


Decorator = DefaultDomain
default_domain = DefaultDomain()
