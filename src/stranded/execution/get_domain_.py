import dataclasses
import typing

from . import decorator
from .abc import get_domain_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetDomain(
    decorator.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
    get_domain_.Decorator[..., typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any, typing.Any],
): ...


Decorator = GetDomain
get_domain = GetDomain()
