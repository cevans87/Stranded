import dataclasses

from .abc import argument_parser_
from .. import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class ArgumentParser(decorator.Decorator, argument_parser_.Decorator): ...


Decorator = ArgumentParser
argument_parser = ArgumentParser()
