import asyncio
import collections
import dataclasses
import gc
import typing
import weakref

import pytest

from stranded.functools.abc import lru_cache_
from stranded.functools.asyncio import LruCache


def get_future_by_key(composed: typing.Any) -> collections.OrderedDict[lru_cache_.Key, typing.Any]:
    enter = composed.stack[-1]
    assert isinstance(enter, lru_cache_.Enter)
    return enter.future_by_key


@pytest.mark.asyncio
async def test_zero_args() -> None:
    call_count = 0

    @LruCache()
    async def foo() -> None:
        nonlocal call_count
        call_count += 1

    await foo()
    await foo()
    assert call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize('arg', [None, 1, 'foo', 0.0])
async def test_primitive_arg(arg: object) -> None:
    call_count = 0

    @LruCache()
    async def foo(_: object) -> int:
        nonlocal call_count
        call_count += 1
        return call_count

    assert await foo(arg) == 1
    assert await foo(arg) == 1
    assert call_count == 1


@pytest.mark.asyncio
async def test_arg_is_not_kept_alive() -> None:
    call_count = 0

    class Arg: ...

    @LruCache()
    async def foo(_: object) -> int:
        nonlocal call_count
        call_count += 1
        return call_count

    arg = Arg()
    arg_ref = weakref.ref(arg)
    assert await foo(arg) == 1
    assert await foo(arg) == 1
    assert call_count == 1
    assert len(get_future_by_key(foo)) == 1

    del arg
    gc.collect()
    assert arg_ref() is None
    assert len(get_future_by_key(foo)) == 0


@pytest.mark.asyncio
async def test_kwarg_is_not_kept_alive() -> None:

    class Arg: ...

    @LruCache()
    async def foo(*, _: object) -> None: ...

    arg = Arg()
    arg_ref = weakref.ref(arg)
    await foo(_=arg)
    assert len(get_future_by_key(foo)) == 1

    del arg
    gc.collect()
    assert arg_ref() is None
    assert len(get_future_by_key(foo)) == 0


@pytest.mark.asyncio
async def test_arg_that_has_no_weak_reference_is_memoized() -> None:
    call_count = 0

    @LruCache()
    async def foo(_: object) -> int:
        nonlocal call_count
        call_count += 1
        return call_count

    # Neither tuples nor their contents support weak references, so the key holds them strongly.
    assert await foo((1, 'foo')) == 1
    assert await foo((1, 'foo')) == 1
    assert call_count == 1
    assert len(get_future_by_key(foo)) == 1


@pytest.mark.asyncio
async def test_equal_args_share_a_memo() -> None:
    call_count = 0

    @dataclasses.dataclass(frozen=True)
    class Arg:
        value: int

    @LruCache()
    async def foo(_: object) -> int:
        nonlocal call_count
        call_count += 1
        return call_count

    # Equal arguments hit the same memo, which lives until the memoized argument itself dies.
    arg, equal_arg, unequal_arg = Arg(value=0), Arg(value=0), Arg(value=1)
    assert await foo(arg) == 1
    assert await foo(equal_arg) == 1
    assert await foo(unequal_arg) == 2
    assert call_count == 2

    del arg
    gc.collect()
    assert await foo(equal_arg) == 3


@pytest.mark.asyncio
async def test_unhashable_arg_raises() -> None:

    @LruCache()
    async def foo(_: object) -> None: ...

    with pytest.raises(TypeError):
        await foo([])


@pytest.mark.asyncio
async def test_method() -> None:
    call_count = 0

    class Foo:
        @LruCache()
        async def foo(self) -> int:
            nonlocal call_count
            call_count += 1
            return call_count

    foo0, foo1 = Foo(), Foo()
    assert await foo0.foo() == 1
    assert await foo0.foo() == 1
    assert call_count == 1

    assert await foo1.foo() == 2
    assert await foo1.foo() == 2
    assert call_count == 2


@pytest.mark.asyncio
async def test_method_does_not_keep_its_instance_alive() -> None:

    class Arg: ...

    class Foo:
        @LruCache()
        async def foo(self, _: object) -> None: ...

    foo, arg = Foo(), Arg()
    await foo.foo(arg)  # type: ignore[arg-type, call-arg]
    foo_ref, arg_ref = weakref.ref(foo), weakref.ref(arg)

    del foo, arg
    gc.collect()
    assert foo_ref() is None
    assert arg_ref() is None


@pytest.mark.asyncio
async def test_classmethod() -> None:
    call_count = 0

    class Foo:
        @classmethod
        @LruCache()
        async def foo(cls) -> None:
            nonlocal call_count
            call_count += 1

    foo0, foo1 = Foo(), Foo()
    await foo0.foo()
    await foo0.foo()
    assert call_count == 1

    await foo1.foo()
    await foo1.foo()
    assert call_count == 1

    await Foo.foo()
    await Foo.foo()
    assert call_count == 1


@pytest.mark.asyncio
async def test_size_expires_memos() -> None:
    call_count = 0

    class Foo:

        @LruCache(size=1)
        async def foo(self, _: object) -> None:
            nonlocal call_count
            call_count += 1

    foo = Foo()
    await foo.foo(0)
    await foo.foo(1)
    await foo.foo(0)
    assert call_count == 3


@pytest.mark.asyncio
async def test_size_method_is_per_instance() -> None:
    call_count = 0

    class Foo:

        @LruCache(size=1)
        async def foo(self, _: object) -> None:
            nonlocal call_count
            call_count += 1

    class Bar(Foo):
        ...

    class Baz(Foo):
        ...

    await asyncio.gather((foo := Foo()).foo(0), (bar := Bar()).foo(0), (baz := Baz()).foo(0))
    assert call_count == 3
    await asyncio.gather(foo.foo(0), bar.foo(0), baz.foo(0))
    assert call_count == 3
    await asyncio.gather(foo.foo(1), bar.foo(1), baz.foo(1))
    assert call_count == 6
    await asyncio.gather(foo.foo(1), bar.foo(1), baz.foo(1))
    assert call_count == 6
    await asyncio.gather(foo.foo(0), bar.foo(0), baz.foo(0))
    assert call_count == 9
    await asyncio.gather(foo.foo(0), bar.foo(0), baz.foo(0))
    assert call_count == 9
    await asyncio.gather(Foo().foo(0), Bar().foo(0), Baz().foo(0))
    assert call_count == 12
    await asyncio.gather(Foo().foo(0), Bar().foo(0), Baz().foo(0))
    assert call_count == 15


@pytest.mark.asyncio
async def test_size_classmethod_is_per_declaration() -> None:
    call_count = 0

    class Foo:

        @classmethod
        @LruCache(size=3)
        async def foo(cls, _: object) -> None:
            nonlocal call_count
            call_count += 1

    class Bar(Foo):
        ...

    class Baz(Foo):
        ...

    await asyncio.gather((foo := Foo()).foo(0), (bar := Bar()).foo(0), (baz := Baz()).foo(0))
    assert call_count == 3
    await asyncio.gather(foo.foo(0), bar.foo(0), baz.foo(0))
    assert call_count == 3
    await asyncio.gather(foo.foo(1), bar.foo(1), baz.foo(1))
    assert call_count == 6
    await asyncio.gather(foo.foo(1), bar.foo(1), baz.foo(1))
    assert call_count == 6
    await asyncio.gather(foo.foo(0), bar.foo(0), baz.foo(0))
    assert call_count == 9
    await asyncio.gather(foo.foo(0), bar.foo(0), baz.foo(0))
    assert call_count == 9
    await asyncio.gather(Foo().foo(0), Bar().foo(0), Baz().foo(0))
    assert call_count == 9
    await asyncio.gather(Foo().foo(0), Bar().foo(0), Baz().foo(0))
    assert call_count == 9


@pytest.mark.asyncio
async def test_size_staticmethod_is_per_declaration() -> None:
    call_count = 0

    class Foo:

        @staticmethod
        @LruCache(size=1)
        async def foo(_: object) -> None:
            nonlocal call_count
            call_count += 1

    class Bar(Foo):
        ...

    class Baz(Foo):
        ...

    await asyncio.gather((foo := Foo()).foo(0), (bar := Bar()).foo(0), (baz := Baz()).foo(0))
    assert call_count == 1
    await asyncio.gather(foo.foo(0), bar.foo(0), baz.foo(0))
    assert call_count == 1
    await asyncio.gather(foo.foo(1), bar.foo(1), baz.foo(1))
    assert call_count == 2
    await asyncio.gather(foo.foo(1), bar.foo(1), baz.foo(1))
    assert call_count == 2
    await asyncio.gather(foo.foo(0), bar.foo(0), baz.foo(0))
    assert call_count == 3
    await asyncio.gather(foo.foo(0), bar.foo(0), baz.foo(0))
    assert call_count == 3
    await asyncio.gather(Foo().foo(0), Bar().foo(0), Baz().foo(0))
    assert call_count == 3
    await asyncio.gather(Foo().foo(0), Bar().foo(0), Baz().foo(0))
    assert call_count == 3


@pytest.mark.asyncio
async def test_herds_only_call_once() -> None:
    asyncio.get_running_loop().set_task_factory(asyncio.eager_task_factory)
    call_count = 0
    event = asyncio.Event()

    @LruCache()
    async def foo() -> None:
        nonlocal call_count
        await event.wait()
        call_count += 1

    futures = [asyncio.get_event_loop().create_task(foo()) for _ in range(10)]
    event.set()
    await asyncio.gather(*futures)

    assert call_count == 1


@pytest.mark.asyncio
async def test_self_referential_return_annotation() -> None:

    @dataclasses.dataclass(eq=False)
    class Foo:
        @LruCache()
        async def foo(self) -> Foo | None:
            return None

    assert await Foo().foo() is None


@pytest.mark.asyncio
async def test_self_referential_return_annotation_classmethod() -> None:

    @dataclasses.dataclass
    class Foo:
        @classmethod
        @LruCache()
        async def foo(cls) -> Foo | None:
            return None

    assert await Foo.foo() is None


@pytest.mark.asyncio
async def test_exceptions_are_saved() -> None:
    call_count = 0

    class FooException(Exception):
        ...

    @LruCache()
    async def foo() -> None:
        nonlocal call_count
        call_count += 1
        raise FooException()

    with pytest.raises(FooException):
        await foo()
    assert call_count == 1

    with pytest.raises(FooException):
        await foo()
    assert call_count == 1
