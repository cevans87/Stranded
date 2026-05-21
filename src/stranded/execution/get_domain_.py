import dataclasses

from . import decorator
from .abc import get_domain_


@dataclasses.dataclass(frozen=True, kw_only=True)
class GetDomain(decorator.Decorator, get_domain_.Decorator): ...


Decorator = GetDomain
get_domain = GetDomain()
