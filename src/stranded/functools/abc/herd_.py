from __future__ import annotations

import abc
import dataclasses
import typing
import weakref

from ...abc import decorator


type GenerateKey = typing.Callable[..., Key]
type Key = typing.Hashable


Raise = decorator.Raise
Stop = decorator.Stop
Param = decorator.Param
Return = decorator.Return


@dataclasses.dataclass(frozen=True, kw_only=True)
class Future[RetT](abc.ABC):

    @abc.abstractmethod
    def set_value(self, value: Return[RetT] | Raise | Stop) -> None: ...

    @abc.abstractmethod
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...

    def __get__(self, instance: decorator.Instance, owner: type[object] | None) -> typing.Self:
        return self


@typing.runtime_checkable
class Decoratee[**ParamT, RetT](
    decorator.Decoratee[ParamT, RetT],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT, FutureT](
    decorator.Exit[ParamT, RetT],
    abc.ABC,
):
    future: FutureT
    key: Key


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT, FutureT](
    decorator.Enter[ParamT, RetT],
    abc.ABC,
):
    # The in-flight-call cache lives on the Enter now that Enter/Exit no longer reach Decorated.
    future_by_key: dict[Key, FutureT] = dataclasses.field(default_factory=dict)

    @staticmethod
    def create_key(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Key:
        return tuple(args), tuple(sorted([*kwargs.items()]))

    def _dispatch(
        self, *args: ParamT.args, **kwargs: ParamT.kwargs,
    ) -> tuple[Exit[ParamT, RetT, Future[RetT]], Decoratee[ParamT, RetT]] | tuple[Future[RetT]]:
        key = self.create_key(*args, **kwargs)
        future = self.future_by_key.get(key)
        match future is None:
            case True:
                future = self.future_by_key[key] = self.decorator.future_t()  # type: ignore[attr-defined]
                return self.exit_t(enter=self, future=future, key=key), self.decoratee  # type: ignore[call-arg, return-value]
            case False:
                return future,
        assert False, "Unreachable"


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**ParamT, RetT](
    decorator.Decorated[ParamT, RetT],
    abc.ABC,
):
    decorated_by_instance: weakref.WeakKeyDictionary[
        decorator.Instance, typing.Self,
    ] = dataclasses.field(default_factory=weakref.WeakKeyDictionary)

    def __get__(self, instance: decorator.Instance, owner: type[object] | None) -> typing.Self:
        if (decorated := self.decorated_by_instance.get(instance)) is not None:
            return decorated
        match self.stack:
            case [*rest, Enter() as enter_]:
                fresh_enter = dataclasses.replace(
                    enter_,
                    decoratee=enter_.decoratee.__get__(instance, owner),
                    future_by_key={},
                )
                return self.decorated_by_instance.setdefault(
                    instance, dataclasses.replace(self, stack=(*rest, fresh_enter)),
                )
        assert False, "unreachable"


@dataclasses.dataclass(frozen=True, kw_only=True)
class Herd[**ParamT, RetT](
    decorator.Decorator[ParamT, RetT],
    abc.ABC,
):
    @property
    @abc.abstractmethod
    def future_t(self) -> type: ...


Decorator = Herd
