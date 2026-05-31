from __future__ import annotations

import abc
import dataclasses
import typing
import weakref

from ...abc import composer


type GenerateKey = typing.Callable[..., Key]
type Key = typing.Hashable


Raise = composer.Raise
Stop = composer.Stop
Param = composer.Param
Return = composer.Return


@dataclasses.dataclass(frozen=True, kw_only=True)
class Future[RetT](abc.ABC):

    @abc.abstractmethod
    def set_value(self, value: Return[RetT] | Raise | Stop) -> None: ...

    @abc.abstractmethod
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...

    def __get__(self, instance: composer.Instance, owner: type[object] | None) -> typing.Self:
        return self


@typing.runtime_checkable
class Composee[**ParamT, RetT](
    composer.Composee[ParamT, RetT],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT, FutureT](
    composer.Exit[ParamT, RetT],
    abc.ABC,
):
    future: FutureT
    key: Key


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT, FutureT](
    composer.Enter[ParamT, RetT],
    abc.ABC,
):
    # The in-flight-call cache lives on the Enter now that Enter/Exit no longer reach Composed.
    future_by_key: dict[Key, FutureT] = dataclasses.field(default_factory=dict)

    @staticmethod
    def create_key(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Key:
        return tuple(args), tuple(sorted([*kwargs.items()]))

    def _dispatch(
        self, *args: ParamT.args, **kwargs: ParamT.kwargs,
    ) -> tuple[Exit[ParamT, RetT, Future[RetT]], Composee[ParamT, RetT]] | tuple[Future[RetT]]:
        key = self.create_key(*args, **kwargs)
        future = self.future_by_key.get(key)
        match future is None:
            case True:
                future = self.future_by_key[key] = self.composer.future_t()  # type: ignore[attr-defined]
                return self.exit_t(enter=self, future=future, key=key), self.composee  # type: ignore[call-arg, return-value]
            case False:
                return future,
        assert False, "Unreachable"


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](
    composer.Composed[ParamT, RetT],
    abc.ABC,
):
    composed_by_instance: weakref.WeakKeyDictionary[
        composer.Instance, typing.Self,
    ] = dataclasses.field(default_factory=weakref.WeakKeyDictionary)

    def __get__(self, instance: composer.Instance, owner: type[object] | None) -> typing.Self:
        if (composed := self.composed_by_instance.get(instance)) is not None:
            return composed
        match self.stack:
            case [*rest, Enter() as enter_]:
                fresh_enter = dataclasses.replace(
                    enter_,
                    composee=enter_.composee.__get__(instance, owner),
                    future_by_key={},
                )
                return self.composed_by_instance.setdefault(
                    instance, dataclasses.replace(self, stack=(*rest, fresh_enter)),
                )
        assert False, "unreachable"


@dataclasses.dataclass(frozen=True, kw_only=True)
class Herd[**ParamT, RetT](
    composer.Composer[ParamT, RetT],
    abc.ABC,
):
    @property
    @abc.abstractmethod
    def future_t(self) -> type: ...


Composer = Herd
