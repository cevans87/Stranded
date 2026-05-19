import abc
import dataclasses
import sys
import typing

from ..abc import decorator


@dataclasses.dataclass(frozen=True)
class Raise(decorator.Raise): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Param[**_Param](decorator.Param[_Param]): ...


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](decorator.Decoratee[_Param, _Ret], typing.Protocol):
    async def __call__(*args: _Param.args, **kwargs: _Param.kwargs) -> _Ret: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Connect[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Exit[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    async def __call__(
        self,
        result: decorator.Raise | _Ret,
    ) -> tuple[_Decoratee | typing.Self | _Enter | _Decorated, ...]:
        return super().__call__(result)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Enter[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    async def __call__(
        self,
        *args: _Param.args,
        **kwargs: _Param.kwargs,
    ) -> tuple[_Decoratee | _Exit | typing.Self | _Decorated, ...]:
        return super().__call__(*args, **kwargs)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Decorated[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    async def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> _Ret:
        result: decorator.Raise | _Ret = ...
        stack = [self, *self.stack]
        while stack:
            match stack.pop():
                case decorator.Param(args=args, kwargs=kwargs): pass
                case Decorated() as decorated_: stack.extend(await decorated_.create_context())
                case Enter() as enter_: stack.extend(await enter_(*args, **kwargs))
                case Exit() as exit_: stack.extend(await exit_(result))
                case Decoratee() as decoratee_:
                    try:
                        result = await decoratee_(*args, **kwargs)
                    except Exception:  # noqa
                        result = decorator.Raise(*sys.exc_info())

        if isinstance(result, decorator.Raise):
            raise result.exc_val

        return result

    async def create_context(self) -> tuple[_Decoratee | _Connect | _Exit | _Enter | _Decorator, ...]:
        return super().create_context()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Decorator[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...
