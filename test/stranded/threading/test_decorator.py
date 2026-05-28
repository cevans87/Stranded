from __future__ import absolute_import

import typing

import pytest

from stranded import Decorator
from stranded.threading.composer import Composer


def test_or_combines_metadata() -> None:
    @Decorator()
    def foo(v: int) -> int:
        """foo doc"""
        return v + 1

    @Decorator()
    def bar(v: int) -> int:
        """bar doc"""
        return v * 2

    combined: typing.Any = Composer()(foo, bar)  # type: ignore[arg-type]

    assert combined.__doc__ == f'{foo.__doc__}\n\n{bar.__doc__}'
    assert combined.__name__ == f'{foo.__name__}, {bar.__name__}'
    assert combined.__qualname__ == f'{foo.__qualname__}, {bar.__qualname__}'
    assert combined.__module__ == f'{foo.__module__}, {bar.__module__}'


def test_or_calls_each_decoratee() -> None:
    calls: list[tuple[str, int]] = []

    @Decorator()
    def foo(v: int) -> int:
        calls.append(('foo', v))
        return v + 1

    @Decorator()
    def bar(v: int) -> int:
        calls.append(('bar', v))
        return v * 10

    @Decorator()
    def baz(v: int) -> int:
        calls.append(('baz', v))
        return v - 3

    result: typing.Any = Composer()(foo, bar, baz).call_sync(7)  # type: ignore[arg-type, attr-defined]

    assert calls == [('foo', 7), ('bar', 8), ('baz', 80)]
    assert result == 77


def test_or_chain_grows() -> None:
    @Decorator()
    def foo(v: int) -> int:
        return v

    @Decorator()
    def bar(v: int) -> int:
        return v

    @Decorator()
    def baz(v: int) -> int:
        return v

    composer = Composer()
    assert len(composer(foo).decorateds) == 1  # type: ignore[arg-type]
    assert len(composer(foo, bar).decorateds) > len(composer(foo).decorateds)  # type: ignore[arg-type]
    assert len(composer(foo, bar, baz).decorateds) > len(composer(foo, bar).decorateds)  # type: ignore[arg-type]


def test_composed_or_extends_with_decorated() -> None:
    @Decorator()
    def foo(v: int) -> int: return v + 1

    @Decorator()
    def bar(v: int) -> int: return v * 10

    @Decorator()
    def baz(v: int) -> int: return v - 3

    composed: typing.Any = Composer()(foo, bar) | baz  # type: ignore[arg-type, operator]
    assert composed.call_sync(7) == 77


def test_composed_or_extends_with_composed() -> None:
    @Decorator()
    def foo(v: int) -> int: return v + 1

    @Decorator()
    def bar(v: int) -> int: return v * 10

    @Decorator()
    def baz(v: int) -> int: return v - 3

    composer = Composer()
    composed: typing.Any = composer(foo, bar) | composer(baz)  # type: ignore[arg-type]
    assert composed.call_sync(7) == 77


if __name__ == '__main__':
    pytest.main()
