from __future__ import absolute_import

import pytest

from stranded import Decorator


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

    result = (foo | bar | baz)(7)

    assert calls == [('foo', 7), ('bar', 8), ('baz', 80)]
    assert result == 77


def test_composed_or_extends_with_decorated() -> None:
    @Decorator()
    def foo(v: int) -> int: return v + 1

    @Decorator()
    def bar(v: int) -> int: return v * 10

    @Decorator()
    def baz(v: int) -> int: return v - 3

    composed = (foo | bar) | baz
    assert composed(7) == 77


def test_composed_or_extends_with_composed() -> None:
    @Decorator()
    def foo(v: int) -> int: return v + 1

    @Decorator()
    def bar(v: int) -> int: return v * 10

    @Decorator()
    def baz(v: int) -> int: return v - 3

    @Decorator()
    def qux(v: int) -> int: return v + 100

    composed = (foo | bar) | (baz | qux)
    assert composed(7) == 177


if __name__ == '__main__':
    pytest.main()
