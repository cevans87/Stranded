import dataclasses
import importlib
import inspect
import typing

from .abc import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT](
    decorator.Decorator[ParamT, RetT, DecorateeT, ReceiveT, SendT, ExitT, EnterT, DecoratedT, DecoratorT],
):

    def __call__[DecorateeT](self, decoratee: DecorateeT) -> DecorateeT:  # type: ignore[override, misc]
        (name_parts := self.__module__.split('.')).insert(
            -1,
            'asyncio' if inspect.iscoroutinefunction(decoratee) else 'threading'
        )

        return importlib.import_module(  # type: ignore[no-any-return]
            name='.'.join(name_parts),
        ).Decorator(**dataclasses.asdict(self))(decoratee)  # noqa
