import dataclasses
import importlib
import inspect

from .abc_ import decorator as abc_decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator(abc_decorator.Decorator):

    def __call__[_Decoratee](self, decoratee: _Decoratee) -> _Decoratee:
        return importlib.import_module(
            name=(
                f'.{"asyncio_" if inspect.iscoroutinefunction(decoratee) else "threading_"}'
                f'.{self.__class__.__module__.split(".")[-1]}'
            ),
            package=__package__,
        ).Decorator(**dataclasses.asdict(self))(decoratee)  # noqa
