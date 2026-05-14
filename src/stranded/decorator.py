import dataclasses
import importlib
import inspect

from .abc import decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(decorator.Decorator):

    def __call__[_Decoratee](self, decoratee: _Decoratee) -> _Decoratee:
        (name_parts := self.__module__.split('.')).insert(
            -1,
            'asyncio' if inspect.iscoroutinefunction(decoratee) else 'threading'
        )

        return importlib.import_module(
            name='.'.join(name_parts),
        ).Decorator(**dataclasses.asdict(self))(decoratee)  # noqa
