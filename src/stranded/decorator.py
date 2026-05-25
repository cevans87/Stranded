import dataclasses
import importlib
import inspect
import typing

from . import composer
from .abc import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**ParamT, RetT](decorator.Decorator[ParamT, RetT]):
    # Stub bindings for the agnostic dispatcher — never instantiated, since
    # __call__ delegates to the asyncio/threading concrete Decorator.
    decoratee_t: typing.ClassVar = decorator.Decoratee
    exit_t: typing.ClassVar = decorator.Exit
    enter_t: typing.ClassVar = decorator.Enter
    decorated_t: typing.ClassVar = decorator.Decorated
    composer_t: typing.ClassVar = composer.Composer

    def __call__[DecorateeT](self, decoratee: DecorateeT) -> DecorateeT:  # type: ignore[override]
        (name_parts := self.__module__.split('.')).insert(
            -1,
            'asyncio' if inspect.iscoroutinefunction(decoratee) else 'threading'
        )

        return importlib.import_module(  # type: ignore[no-any-return]
            name='.'.join(name_parts),
        ).Decorator(**dataclasses.asdict(self))(decoratee)  # noqa
