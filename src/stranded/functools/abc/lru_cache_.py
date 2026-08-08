from __future__ import annotations

import abc
import collections
import contextlib
import dataclasses
import itertools
import typing
import weakref
import sys

from ...abc import composer_
from ...builtins import exception_


type GenerateKey = typing.Callable[..., Key]
type FutureByKey = collections.OrderedDict[Key, typing.Any]


Raise = composer_.Raise
Stop = composer_.Stop
Param = composer_.Param
Return = composer_.Return


class Exception(exception_.Exception): ...  # noqa


@typing.final
class Ref[T](weakref.ref[T]):
    """Weak reference to a memoized argument that evicts its cache entry when the referent dies.

    Hashes and compares like the referent while the referent is alive, so that `Key`s built from
    equal arguments are equal. The referent's hash is cached at construction, which keeps the key
    hashable - and therefore removable from the cache - after the referent is gone.
    """
    __slots__ = ('future_by_key', 'key')

    future_by_key: weakref.ref[FutureByKey] | None
    key: Key | None

    def __new__(cls, referent: T) -> typing.Self:
        return super().__new__(cls, referent, cls.__discard)

    def __init__(self, referent: T) -> None:
        super().__init__(referent, type(self).__discard)  # type: ignore[call-arg]
        self.future_by_key = None
        self.key = None
        hash(self)  # Cache the referent's hash while the referent is still alive.

    def __discard(self) -> None:
        # Called with this (now dead) reference as `self` once the referent is garbage collected.
        if (future_by_key_ref := self.future_by_key) is None or (key := self.key) is None:
            return
        if (future_by_key := future_by_key_ref()) is not None:
            future_by_key.pop(key, None)

    def bind(self, future_by_key: weakref.ref[FutureByKey], key: Key) -> None:
        """Discard `key` from `future_by_key` once the referent dies."""
        self.future_by_key = future_by_key
        self.key = key


def create_ref(value: typing.Any) -> typing.Hashable:
    """Refer to `value` weakly if it supports weak references, and strongly otherwise."""
    try:
        return Ref(value)
    except TypeError:
        # `value` either does not support weak references (e.g. `int`, `str`, and `tuple`) or is
        # unhashable, in which case caching it fails the same way an unhashable key always has.
        return typing.cast(typing.Hashable, value)


@typing.final
@dataclasses.dataclass(frozen=True, kw_only=True)
class Key:
    """Cache key that refers to the memoized arguments weakly wherever it can.

    Keeping arguments alive for as long as they are memoized would leak every argument that a cache
    ever saw, so arguments that support weak references are stored as `Ref`s. Note that an argument
    that supports weak references only indirectly - a `tuple` of objects, say - is still stored
    strongly, since there is nothing to hang a reference on.
    """
    args: tuple[typing.Hashable, ...]
    kwargs: tuple[tuple[str, typing.Hashable], ...]

    @classmethod
    def create(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Self:
        return cls(
            args=tuple(create_ref(arg) for arg in args),
            kwargs=tuple((name, create_ref(kwargs[name])) for name in sorted(kwargs)),
        )

    @property
    def refs(self) -> typing.Iterator[Ref[typing.Any]]:
        """The weak references that this key is made of."""
        return (
            value
            for value in itertools.chain(self.args, (value for _, value in self.kwargs))
            if isinstance(value, Ref)
        )

    def bind(self, future_by_key: FutureByKey) -> None:
        """Discard this key from `future_by_key` as soon as any of its weak arguments dies."""
        future_by_key_ref = weakref.ref(future_by_key)
        for ref in self.refs:
            ref.bind(future_by_key_ref, self)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Future[RetT](abc.ABC):

    @abc.abstractmethod
    def set_value(self, value: Return[RetT] | Raise | Stop) -> None: ...

    @abc.abstractmethod
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...

    def __get__(self, instance: composer_.Instance, owner: type[object] | None) -> typing.Self:
        return self


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT, FutureT](composer_.Exit[ParamT, RetT], abc.ABC):
    future: FutureT
    key: Key


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT, FutureT](composer_.Enter[ParamT, RetT], abc.ABC):
    future_by_key: collections.OrderedDict[Key, FutureT] = dataclasses.field(default_factory=collections.OrderedDict)

    @staticmethod
    def create_key(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Key:
        return Key.create(*args, **kwargs)

    def get_future(self, key: Key) -> FutureT | None:
        """Return the future memoized for `key`, if any, marking it as the most recently used."""
        if (future := self.future_by_key.get(key)) is not None:
            # A weak argument may have died - taking its entry with it - since the get.
            with contextlib.suppress(KeyError):
                self.future_by_key.move_to_end(key)
        return future

    def set_future(self, key: Key) -> FutureT:
        """Memoize and return a new future for `key`, evicting the least recently used entries."""
        while self.composer.size <= len(self.future_by_key):  # type: ignore[attr-defined]
            self.future_by_key.popitem(last=False)
        future: FutureT = self.composer.future_t()  # type: ignore[attr-defined]
        self.future_by_key[key] = future
        key.bind(self.future_by_key)
        return future


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], abc.ABC):
    # Enters rather than whole bound compositions: a bound composition holds the bound composee,
    # which refers back to the instance that keys it here, and so would outlive it forever.
    enter_by_instance: weakref.WeakKeyDictionary[
        composer_.Instance, composer_.EnterT[ParamT, RetT],
    ] = dataclasses.field(default_factory=weakref.WeakKeyDictionary)

    @typing.override
    def create_enter(self, instance: composer_.Instance) -> composer_.EnterT[ParamT, RetT]:
        if (enter := self.enter_by_instance.get(instance)) is not None:
            return enter
        match self.enter:
            case Enter() as enter_:
                return self.enter_by_instance.setdefault(
                    instance, dataclasses.replace(enter_, future_by_key=collections.OrderedDict()),
                )
        assert False, "unreachable"


@dataclasses.dataclass(frozen=True, kw_only=True)
class LruCache[**ParamT, RetT](composer_.Composer[ParamT, RetT], abc.ABC):
    size: int = sys.maxsize

    @property
    @abc.abstractmethod
    def future_t(self) -> type: ...


Composer = LruCache
