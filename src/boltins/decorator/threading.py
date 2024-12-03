import abc
import dataclasses
import sys
import typing

from . import common


@dataclasses.dataclass(frozen=True)
class Raise(common.Raise): ...


@typing.runtime_checkable
class Decoratee[** Param, Ret](common.Decoratee[Param, Ret], typing.Protocol):

    def __call__(*args: Param.args, **kwargs: Param.kwargs) -> Ret: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[_Enter, _Ret](common.Exit[_Enter, _Ret], abc.ABC):

    def __call__(self, result: common.Raise | _Ret) -> ():
        return tuple()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[_Decoratee, _Exit, _Decorated, **_Param](common.Enter[_Decoratee, _Exit, _Decorated, _Param], abc.ABC):

    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> tuple[_Exit, _Decoratee]:
        return super().__call__(*args, **kwargs)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[_Decoratee, _Exit, _Enter, _Decorator, ** _Param, _Ret](
    common.Decorated[_Decoratee, _Exit, _Enter, _Decorator],
    abc.ABC,
):
    @typing.final
    def __call__(self, *args: _Param.args, **kwargs: _Param.kwargs) -> _Ret:
        result: common.Raise | _Ret = ...
        stack = [self]
        while stack:
            try:
                match stack.pop():
                    case Decorated() as decorated:
                        stack.append(decorated.decorator.enter_t(decorated=decorated))
                    case Enter() as enter:
                        stack.extend(enter(*args, **kwargs))
                    case Exit() as exit_:
                        stack.extend(exit_(result))
                    case Decoratee() as decoratee:
                        result = decoratee(*args, **kwargs)
            except Exception:  # noqa
                result = common.Raise(*sys.exc_info())

        if isinstance(result, common.Raise):
            raise result.exc_val

        return result


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[_Decoratee, _Exit, _Enter, _Decorated](
    common.Decorator[_Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
): ...
