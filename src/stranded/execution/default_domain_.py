import dataclasses

from . import decorator
from .abc import default_domain_


@dataclasses.dataclass(frozen=True, kw_only=True)
class DefaultDomain(decorator.Decorator, default_domain_.Decorator): ...


Decorator = DefaultDomain
default_domain = DefaultDomain()
