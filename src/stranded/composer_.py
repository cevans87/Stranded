import dataclasses
import importlib
import inspect
import typing

from .abc import composer_


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composer[**ParamT, RetT](composer_.Composer[ParamT, RetT]):
    # Stub bindings for the agnostic dispatcher — never instantiated, since
    # __call__ delegates to the asyncio/threading concrete Composer.
    composee_t: typing.ClassVar = composer_.Composee
    connect_t: typing.ClassVar = composer_.Connect
    exit_t: typing.ClassVar = composer_.Exit
    enter_t: typing.ClassVar = composer_.Enter
    composed_t: typing.ClassVar = composer_.Composed

    def __call__[ComposeeT](self, composee: ComposeeT) -> ComposeeT:  # type: ignore[override]
        (name_parts := self.__module__.split('.')).insert(
            -1,
            'asyncio' if inspect.iscoroutinefunction(composee) else 'threading'
        )

        return importlib.import_module(  # type: ignore[no-any-return]
            name='.'.join(name_parts),
        ).Composer(**dataclasses.asdict(self))(composee)  # noqa
