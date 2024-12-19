import dataclasses
import importlib
import inspect

from .abc_ import decorator as abc_decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(abc_decorator.Decorator):

    def __call__[_Decoratee](self, decoratee: _Decoratee) -> _Decoratee:
        (name_parts := self.__module__.split('.')).insert(
            -1,
            'asyncio_' if inspect.iscoroutinefunction(decoratee) else 'threading_'
        )

        return importlib.import_module(
            name='.'.join(name_parts),
        ).Decorator(**dataclasses.asdict(self))(decoratee)  # noqa
