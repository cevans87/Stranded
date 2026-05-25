import dataclasses
import functools
import importlib
import inspect
import typing

from ..abc import decorator


def _is_async(obj: object) -> bool:
    if inspect.iscoroutinefunction(obj):
        return True
    call = getattr(obj, '__call__', None)
    return call is not None and inspect.iscoroutinefunction(call)


def _is_promotable(obj: object) -> bool:
    """A field is promotable to async only if it's a plain function or method.

    Class instances (e.g. Scheduler) are callable but shouldn't be wrapped — their
    own variant-aware __call__ is what callers should use.
    """
    return inspect.isfunction(obj) or inspect.ismethod(obj)


def _to_async(obj: typing.Callable[..., typing.Any]) -> typing.Callable[..., typing.Any]:
    if _is_async(obj):
        return obj

    @functools.wraps(obj)
    async def _wrapped(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return obj(*args, **kwargs)

    return _wrapped


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
):
    def __call__[DecorateeT](self, decoratee: DecorateeT) -> DecorateeT:  # type: ignore[override]
        promotable = {
            field.name: getattr(self, field.name)
            for field in dataclasses.fields(self)
            if _is_promotable(getattr(self, field.name))
        }
        any_async = _is_async(decoratee) or any(_is_async(v) for v in promotable.values())

        if any_async:
            self_ = dataclasses.replace(self, **{k: _to_async(v) for k, v in promotable.items()})
            decoratee = _to_async(decoratee)  # type: ignore[arg-type, assignment]
            target = 'asyncio'
        else:
            self_ = self
            target = 'threading'

        name_parts = self_.__module__.split('.')
        name_parts.insert(-1, target)

        return importlib.import_module(  # type: ignore[no-any-return]
            name='.'.join(name_parts),
        ).Decorator(**{f.name: getattr(self_, f.name) for f in dataclasses.fields(self_)})(decoratee)
