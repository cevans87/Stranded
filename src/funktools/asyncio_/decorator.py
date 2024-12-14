import abc
import dataclasses
import sys
import typing

from ..abc_ import decorator


@dataclasses.dataclass(frozen=True)
class Raise(decorator.Raise): ...


@typing.runtime_checkable
class Decoratee[** Param, Ret](decorator.Decoratee, typing.Protocol):

    async def __call__(*args: Param.args, **kwargs: Param.kwargs) -> Ret: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Exit: typing.Self, _Enter, _Decorated, _Decorator](
    decorator.Exit[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    async def __call__(self, result: decorator.Raise | _Ret) -> ():
        return super().__call__(result)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret, _Decoratee, _Exit, _Enter: typing.Self, _Decorated, _Decorator](
    decorator.Enter[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    async def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Exit, _Decoratee]:
        return super().__call__(*args, **kwargs)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated: typing.Self, _Decorator](
    decorator.Decorated[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    async def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> _Ret:
        result: decorator.Raise | _Ret = ...
        stack = list(self.create_stack())
        while stack:
            try:
                match stack.pop():
                    case Enter() as enter:
                        stack.extend(await enter(*args, **kwargs))
                    case Exit() as exit_:
                        stack.extend(await exit_(result))
                    case Decoratee() as decoratee:
                        result = await decoratee(*args, **kwargs)
            except Exception:  # noqa
                result = decorator.Raise(*sys.exc_info())

        if isinstance(result, decorator.Raise):
            raise result.exc_val

        return result


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator: typing.Self](
    decorator.Decorator[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...
